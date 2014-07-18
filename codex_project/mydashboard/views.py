import json
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from actors.models import Node, SensorMap, Reading, Sensor
from actors.managers import ReadingsManager
import datetime

#-------------------------------------------------------------------------------
@csrf_exempt
def new_node_api(request):
    '''
    API HTTP POST call to add new node
    HTTP parameters: deployment, node_type, node_id, authentication_key
                     encryption_key, group_key, ota_key
    '''

    data = request.POST

    return HttpResponse("Error creating new node.", status=404)


#-------------------------------------------------------------------------------
class HomeView(TemplateView):
    '''
    A Template View to display home dashboard
    '''


    template_name = 'home.html'


    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        # nodes = self.get_node_info()
        # modality = SensorMap.objects.filter()
        # ctx.update({
        #         'nodes': nodes,
        #         'modalities': modality
        #     })
        # return ctx

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
    timestamp = data.get('timestamp', None)
    node_id = kwargs.get('node_id', None)
    sensor_id = data.get('sensor_id', None)
    readings = data.get('readings', None)
    if seqno is None or node_id is None or timestamp is None or sensor_id is None:
        return HttpResponse(status=404)

    try:
        node = Node.objects.get(node_id=node_id)
    except Node.DoesNotExist:
        return HttpResponse(status=404)

    try:
        sensorMap = SensorMap.objects.get(modality_bit=sensor_id, app_config=node.app_config)
    except SensorMap.DoesNotExist:
        return HttpResponse(status=404)

    reading = Reading.objects.add_reading(timestamp, seqno, node, sensorMap.sensor,
                readings)

    response_data = {}
    response_data['status'] = {'code': 200,
                                'timestamp': timestamp,
                                'message': reading[1]
                            }

    response_data['node'] = { 'id': node.node_id,
                            'type': node.get_node_type_display(),
                            'app_config': node.app_config.config_id
                }

    response_data['sensor'] = { 'modality': sensorMap.sensor.modality,
                                'data_format': sensorMap.sensor.data_format,
                                'value': readings
                                }

    return HttpResponse(json.dumps(response_data), status=200, content_type="application/json")

#-------------------------------------------------------------------------------
@csrf_exempt
def get_readings_api(request, **kwargs):
    '''
    API HTTP POST call to send node readings
    HTTP parameters: seqno, timestamp, node_id, sensor_id, readings
    '''

    data = request.GET
    source = data.get('source', None)
    destination = data.get('destination', None)

    readings = Reading.objects.get_readings(source, destination)

    import pdb; pdb.set_trace()
    response_data = {}
    response_data['status'] = {'code': 200,
                                'timestamp': datetime.datetime.now(),
                                'message': reading[1]
                            }


    response_data['readings'] = {
                                'value': readings
                                }

    return HttpResponse(json.dumps(response_data), status=200, content_type="application/json")
