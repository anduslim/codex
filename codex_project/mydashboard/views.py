import json
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import mosquitto
from django.conf import settings
from actors.models import Deployment, Node, SensorMap, Key, Comments
from key_generation.keygenerator import KeyGenerator
from cert_generation.certgeneration import CertGenerator

import redis


SENSORREG_BACKEND = 4;
SENSORKEY_REQUEST = 5;
SERVER_KEY_UPDATE = 6;
SENSORKEY_REQUEST_ACK = 7;


def home(request):
    """ Default view for the root """
    nodes = Node.objects.filter()

    return render(request, 'base/home.html')

#-------------------------------------------------------------------------------
@csrf_exempt
def get_master_key_api(request, **kwargs):
    '''
    API HTTP Get call to retrieve master key from backend
    HTTP parameters: deployment_id
    '''

    deployment_id = kwargs.get('deployment_id', None)

    try:
        deployment = Deployment.objects.get(id=deployment_id)
    except Deployment.DoesNotExist:
        print("Deployment Id does not exist")
        return HttpResponse('<h2>Error. Deployment ID does not exist!</h>', status=404)

    result = Deployment.objects.get_master_key(deployment_id)

    response_data = {}
    response_data['status'] = '200 OKAY'
    response_data['master_key'] = result

    return HttpResponse(json.dumps(response_data), status=200, content_type="application/json");


#-------------------------------------------------------------------------------
@csrf_exempt
def get_node_key_api(request, **kwargs):
    '''
    API HTTP Get call to retrieve keys for node from backend
    HTTP parameters: node_id
    '''

    node_id = kwargs.get('node_id', None)

    result = get_node_key(node_id)
    if result is None:
        return HttpResponse('<h2>Error. Node ID does not exist!</h>', status=404)

    response_data = {}
    response_data['status'] = '200 OKAY'
    response_data['keys'] = result
    response_data['type'] = SENSORKEY_REQUEST

    return HttpResponse(json.dumps(response_data), status=200, content_type="application/json")

#-------------------------------------------------------------------------------
@csrf_exempt
def get_OTA_key_api(request, **kwargs):
    '''
    API HTTP Get call to retrieve only the otakey for node from backend
    HTTP parameters: node_id, imei
    '''

    node_id = kwargs.get('node_id', None)
    imei = kwargs.get('imei', None)

    result = get_node_key(node_id, 'OTAK')
    if result is None:
        return HttpResponse('<h2>Error. Node ID does not exist!</h>', status=404)

    response_data = {}
    response_data['status'] = '200 OKAY'
    response_data['keys'] = result

    return HttpResponse(json.dumps(response_data), status=200, content_type="application/json")


#-------------------------------------------------------------------------------
def get_node_key(node_id, key_type=None, pkt_type=None):
    '''
    Get node key from model
    input:  node_id
    return: node keys
    '''

    try:
        node = Node.objects.filter(node_id=node_id)[0]
    except Node.DoesNotExist:
        print("Node Id does not exist")
        return None
    except IndexError:
        print("IndexError.")
        return None

    response = {}
    result = Node.objects.get_key(node_id, key_type)
    response['keys'] = result
    if pkt_type is not None:
        response['type'] = pkt_type

    return json.dumps(response)


#-------------------------------------------------------------------------------
@csrf_exempt
def register_node_api(request, **kwargs):
    '''
    API HTTP POST call to register node
    HTTP parameters: deployment, node_type, node_id
    '''

    data = request.POST
    deployment_id = data.get('deployment', None)
    node_id = kwargs.get('node_id', None)
    is_register = data.get('registration', None)
    if deployment_id is None or node_id is None or is_register is None:
        return HttpResponse(status=404)
    deployment = Deployment.objects.get(id=deployment_id)

    node = Node.objects.get(node_id=node_id, deployment=deployment)
    node.registration_status = is_register in 'True'
    node.save()

    response_data = {}
    response_data['status'] = '200 UPDATED'
    response_data['node'] = { 'id': node.id,
                        'deployment_name': node.deployment.name,
                        'node_type': node.get_node_type_display(),
                        'registration_status': node.registration_status
                }

    return HttpResponse(json.dumps(response_data), status=200, content_type="application/json")

#-------------------------------------------------------------------------------

class GenerateKeys(View):
    '''
    AJAX call to generate keys
    '''

    def get(self, request):
        data = request.GET
        deployment_name = str(data.get('node_deployment', None))
        try:
            deployment = Deployment.objects.get(name=deployment_name)
        except Deployment.DoesNotExist:
            print("Deployment does not exist")
            raise HttpResponseNotFound(content=dict(error_code=404, error_msg="Deployment does not exist"));

        try:
            node_id = int(data.get('node_id', None))
            if node_id is None:
                print("Node ID is not passed in")
                raise HttpResponseNotFound(content=dict(error_code=404, error_msg="Node ID is invalid"));
        except TypeError as e:
            raise HttpResponseNotFound(content=dict(error_code=404, error_msg="Node ID is invalid"));

        parse_keys, raw_keys = KeyGenerator.generate_keys(deployment.id, node_id)

        payload = {}
        response_data = {}

        for key in parse_keys:
            key,value = key.split('=')
            payload[key] = value
        payload['node_id'] = node_id

        return HttpResponse(json.dumps(payload), content_type="application/json")


#-------------------------------------------------------------------------------
@csrf_exempt
def new_node_api(request):
    '''
    API HTTP POST call to add new node
    HTTP parameters: deployment, node_type, node_id, authentication_key
                     encryption_key, group_key, ota_key
    '''

    data = request.POST
    deployment_name = str(data.get('deployment', None))
    try:
        deployment = Deployment.objects.get(name=deployment_name)
    except Deployment.DoesNotExist:
        print("Deployment does not exist")
        return HttpResponse("Deployment does not exist", status=404)

    try:
        node_id = int(data.get('node_id', None))
        if node_id is None:
            print("Node ID is not passed in")
            return HttpResponse("Node ID is invalid.", status=404)
    except TypeError as e:
        return HttpResponse("Please key in an integer for node ID.", status=404)

    try:
        node_type = int(data.get('node_type', None))
        if node_type not in dict(Node.NODES_CHOICES):
            print("Node Type does not exist")
            return HttpResponse("Node type does not exist!", status=404)
    except TypeError as e:
        return HttpResponse("Please key in an integer for node type.", status=404)

    parse_keys, raw_keys = KeyGenerator.generate_keys(deployment.id, node_id)
    result, node = KeyGenerator.update_backend_keys(deployment, node_id, node_type, parse_keys)

    print("Result" + str(result) + "\nReceived: " + str(data) +"\n");


    if result is True:
        response_data = {}
        response_data['status'] = '201 CREATED'
        response_data['node'] = { 'gid': node.id,
                            'deployment_name': node.deployment.name,
                            'node_id': node.node_id,
                            'node_type': node.get_node_type_display(),
                            'key_version': node.key_version,
                            'authentication_key': node.authentication_key.key_value,
                            'encryption_key': node.encryption_key.key_value,
                            'group_key': node.group_key.key_value,
                            'ota_key': node.ota_key.key_value,
                            'raw_keys': raw_keys
                    }

        return HttpResponse(json.dumps(response_data), status=201, content_type="application/json")
    else:
        return HttpResponse("Error creating new node.", status=404)

#-------------------------------------------------------------------------------
@csrf_exempt
def node_api(request):
    try:
        #Get User from sessionid
        # session = Session.objects.get(session_key=request.POST.get('sessionid'))
        # user_id = session.get_decoded().get('_auth_user_id')
        # user = User.objects.get(id=user_id)

        #Create comment
        Comments.objects.create(modality=request.POST.get('modality'), reading=request.POST.get('reading'))

        #Once comment has been created post it to the chat channel
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('chat', request.POST.get('modality') + ': ' + request.POST.get('reading'))

        return HttpResponse("Everything worked :)")
    except Exception as e:
        return HttpResponseServerError(str(e))

#-------------------------------------------------------------------------------
class HomeView(TemplateView):
    '''
    A Template View to display home dashboard
    '''

    COMMAND_TYPE_SECURITY = 1
    COMMAND_TYPE_NODE = 2
    TOPIC_PREFIX = "sns"
    TOPIC_DOWNLINK = "nm"
    TOPIC_SAM_MODULE = "sam"
    TOPIC_SECURITY_MODULE = "security"


    template_name = 'base/home.html'

    def keys_C_format(self, key):
        result = ""
        tempBuf = ""
        for index, shex in enumerate(key):
            tempBuf += shex
            if index%2 == 1:
                result += '0x' + tempBuf
                if index != (len(key)-1):
                    result += ', '
                tempBuf = ""
        return result

    def post(self, request, *args, **kwargs):
        ##Update merchant status via POST

        data = request.POST
        nodeID = data.get('node_ID', None)
        deploymentName = data.get('node_deployment', None)
        command = data.get('node_command-' + nodeID, None)
        device = data.get('device-' + nodeID, None)
        module = None
        try:
            node = Node.objects.filter(node_id=nodeID)[0]
        except Node.DoesNotExist:
            print("Node Id does not exist")
            return None
        except IndexError:
            print("IndexError.")
            return None

        if command == str(self.COMMAND_TYPE_NODE):
            module = self.TOPIC_SAM_MODULE
            interval_type = data.get('interval_type', None)
            if interval_type == 'send':
                interval = data.get('send_int-' + nodeID, None)
                number = device
            elif interval_type == 'sense':
                interval = data.get('sense_int-' + nodeID, None)
                number = data.get('sensor-' + nodeID, None)
            result = interval_type + "," + number + "," + interval

        elif command == str(self.COMMAND_TYPE_SECURITY):
            module = self.TOPIC_SECURITY_MODULE
            EK = data.get('encryption_key-' + nodeID)
            AK = data.get('authentication_key-' + nodeID)
            GK = data.get('group_key-' + nodeID)
            OTAK = data.get('ota_key-' + nodeID)
            result = {'key_version': node.key_value, 'AK': self.keys_C_format(AK), 'EK': self.keys_C_format(EK), 'OTAK': self.keys_C_format(OTAK), 
            'GK': self.keys_C_format(GK)}
            response = {}
            response['keys'] = result
            response['type'] = SERVER_KEY_UPDATE

        if module is not None:
            mqttc = mosquitto.Mosquitto()
            mqttc.connect(settings.EXT_BROKER_URL, settings.EXT_BROKER_PORT, settings.EXT_BROKER_TIMEOUT)
            mqttc.publish(self.TOPIC_PREFIX + "/" + deploymentName + "/" + \
                nodeID + "/" + self.TOPIC_DOWNLINK + "/" + module, json.dumps(response), 1)
            mqttc.disconnect();
            messages.add_message(request, messages.SUCCESS, "Command for node " + nodeID + " sent!")
        else:
            messages.add_message(request, messages.ERROR, "Command for node " + nodeID + " not successful!")


        return redirect('mydashboard:dashboard')

    def get_node_info(self):
        active_node = []
        inactive_node = []

        nodes = Node.objects.filter()

        for node in nodes:
            if node.registration_status:
                active_node.append(node)
            else:
                inactive_node.append(node)

        return {
                'active_node': active_node,
                'inactive_node': inactive_node
        }

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        nodes = self.get_node_info()
        modality = SensorMap.objects.filter()
        ctx.update({
                'nodes': nodes,
                'modalities': modality
            })
        return ctx

    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)


#-------------------------------------------------------------------------------
class NodeNewView(TemplateView):
    '''
    A Template View to create a new node
    '''

    template_name = 'access/sensor_new.html'

    def post(self, request, *args, **kwargs):
        ##Update merchant status via POST

        data = request.POST
        deployment_id = data.get('deployment', None)
        deployment = Deployment.objects.get(id=deployment_id)
        node_type = int(data.get('node_type', None))

        authentication_key = data.get('authentication_key', None)
        AK = Key.objects.create_key(Key.AUTHENTICATION_KEY, authentication_key)

        encryption_key = data.get('encryption_key', None)
        EK = Key.objects.create_key(Key.ENCRYPTION_KEY, encryption_key)

        group_key = data.get('group_key', None)
        GK = Key.objects.create_key(Key.GROUP_KEY, group_key)

        ota_key = data.get('ota_key', None)
        OTAK = Key.objects.create_key(Key.OTA_KEY, ota_key)

        node = Node.objects.create_node(deployment, node_type, EK, AK, GK, OTAK)

        messages.add_message(request, messages.SUCCESS, "Node " + str(node.id) + " created!")

        return redirect('mydashboard:sensor')

    def get_context_data(self, **kwargs):
        ## Display merchant status in template
        node_type_options = {}
        ctx = super(NodeNewView, self).get_context_data(**kwargs)

        deployment = Deployment.objects.filter()
        node_type = Node.NODES_CHOICES

        ctx.update({
                'deployments': deployment,
                'node_types': node_type
            })
        return ctx

    def dispatch(self, *args, **kwargs):
        return super(NodeNewView, self).dispatch(*args, **kwargs)

#-------------------------------------------------------------------------------
class ReadingsView(TemplateView):
    '''
    A Template View to display readings dashboard
    '''

    template_name = 'base/readings.html'

    def get_node_info(self):
        active_node = []
        inactive_node = []

        nodes = Node.objects.filter()

        for node in nodes:
            if node.registration_status:
                active_node.append(node)
            else:
                inactive_node.append(node)

        return {
                'active_node': active_node,
                'inactive_node': inactive_node
        }

    def get_context_data(self, **kwargs):
        ctx = super(ReadingsView, self).get_context_data(**kwargs)

        comments = Comments.objects.select_related().all()[0:100]
        modality = SensorMap.objects.filter()
        nodes = self.get_node_info()
        ctx.update({
                'nodes': nodes,
                'comments': comments,
                'modalities': modality
            })
        return ctx

    def dispatch(self, *args, **kwargs):
        return super(ReadingsView, self).dispatch(*args, **kwargs)

#-------------------------------------------------------------------------------
class CertificatesView(TemplateView):
    '''
    A Template View to display readings dashboard
    '''

    template_name = 'base/certificates.html'

    def post(self, request, *args, **kwargs):
        data = request.POST

        common_name = data.get('common_name', None)
        cert_name = data.get('cert_name', None)
        # import pdb; pdb.set_trace()
        if not common_name or not cert_name :
            messages.add_message(request, messages.WARNING, "Please input the names of certificate!")
        else:
            messages.add_message(request, messages.SUCCESS, "Certificate created!")

        return redirect('mydashboard:certificates')


    def get_context_data(self, **kwargs):
        ctx = super(CertificatesView, self).get_context_data(**kwargs)

        return ctx

    def dispatch(self, *args, **kwargs):
        return super(CertificatesView, self).dispatch(*args, **kwargs)

