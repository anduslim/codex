import json
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from actors.models import Node, SensorMap

#-------------------------------------------------------------------------------
@csrf_exempt
def new_node_api(request):
    '''
    API HTTP POST call to add new node
    HTTP parameters: deployment, node_type, node_id, authentication_key
                     encryption_key, group_key, ota_key
    '''

    data = request.POST
    # deployment_name = str(data.get('deployment', None))
    # try:
    #     deployment = Deployment.objects.get(name=deployment_name)
    # except Deployment.DoesNotExist:
    #     print("Deployment does not exist")
    #     return HttpResponse("Deployment does not exist", status=404)

    # try:
    #     node_id = int(data.get('node_id', None))
    #     if node_id is None:
    #         print("Node ID is not passed in")
    #         return HttpResponse("Node ID is invalid.", status=404)
    # except TypeError as e:
    #     return HttpResponse("Please key in an integer for node ID.", status=404)

    # try:
    #     node_type = int(data.get('node_type', None))
    #     if node_type not in dict(Node.NODES_CHOICES):
    #         print("Node Type does not exist")
    #         return HttpResponse("Node type does not exist!", status=404)
    # except TypeError as e:
    #     return HttpResponse("Please key in an integer for node type.", status=404)

    # parse_keys, raw_keys = KeyGenerator.generate_keys(deployment.id, node_id)
    # result, node = KeyGenerator.update_backend_keys(deployment, node_id, node_type, parse_keys)

    # print("Result" + str(result) + "\nReceived: " + str(data) +"\n");


    # if result is True:
    #     response_data = {}
    #     response_data['status'] = '201 CREATED'
    #     response_data['node'] = { 'gid': node.id,
    #                         'deployment_name': node.deployment.name,
    #                         'node_id': node.node_id,
    #                         'node_type': node.get_node_type_display(),
    #                         'key_version': node.key_version,
    #                         'authentication_key': node.authentication_key.key_value,
    #                         'encryption_key': node.encryption_key.key_value,
    #                         'group_key': node.group_key.key_value,
    #                         'ota_key': node.ota_key.key_value,
    #                         'raw_keys': raw_keys
    #                 }

    #     return HttpResponse(json.dumps(response_data), status=201, content_type="application/json")
    # else:
    return HttpResponse("Error creating new node.", status=404)


#-------------------------------------------------------------------------------
class HomeView(TemplateView):
    '''
    A Template View to display home dashboard
    '''


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
class ReadingsView(TemplateView):
    '''
    A Template View to display readings dashboard
    '''

    template_name = 'base/readings.html'

    def get_node_info(self):
        active_node = []
        inactive_node = []

        nodes = Node.objects.filter()

        return {
                'active_node': active_node,
                'inactive_node': inactive_node
        }

    def get_context_data(self, **kwargs):
        ctx = super(ReadingsView, self).get_context_data(**kwargs)

        modality = SensorMap.objects.filter()
        nodes = self.get_node_info()
        ctx.update({
                'nodes': nodes,
                'modalities': modality
            })
        return ctx

    def dispatch(self, *args, **kwargs):
        return super(ReadingsView, self).dispatch(*args, **kwargs)

#-------------------------------------------------------------------------------
@csrf_exempt
def post_readings_api(request, **kwargs):
    '''
    API HTTP POST call to send node readings
    HTTP parameters: seqno, timestamp, node_id, sensor_id, readings
    '''

    data = request.POST
    seqno = data.get('seqno', None)
    timestamp = kwargs.get('timestamp', None)
    nodeid = data.get('node_id', None)
    sensor_id = data.get('sensor_id', None)
    readings = data.get('readings', None)
    if seqno is None or nodeid is None or timestamp is None or sensor_id is None:
        return HttpResponse(status=404)

    node = Node.objects.get(node_id=node_id)

    response_data = {}
    response_data['status'] = '200 UPDATED'
    response_data['node'] = { 'id': node.id,
                        'deployment_name': node.deployment.name,
                        'node_type': node.get_node_type_display(),
                        'registration_status': node.registration_status
                }

    return HttpResponse(json.dumps(response_data), status=200, content_type="application/json")
