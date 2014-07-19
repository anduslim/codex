from django.db import models
from datetime import datetime
from actors.haversine import haversine
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils import timezone

class NodesManager(models.Manager):

	def create_node(self, _node_id= None, _node_type=None,  _app_config=None):

		try:
			node = self.model.objects.get()
		except self.model.DoesNotExist:

			node = self.create(node_id=_node_id, node_type=_node_type, app_config=_app_config)

		return node

class ReadingsManager(models.Manager):

    ERROR, CREATED, EXISTS = range(3)
    STATUS_CHOICES = (
        (ERROR, u'Error! Reading not recorded!'),
        (CREATED, u'Success! Reading accepted!'),
        (EXISTS, u'WARNING! Reading exists!')
    )

    def add_reading(self, timestamp=None, seq_no=None, node_id=None, sensor_id=None,
                     readings=None):
        if seq_no != None or node_id != None:
            try:
                self.model.objects.get(seq_no=seq_no, node=node_id)
                status = self.STATUS_CHOICES[self.EXISTS]
            except self.model.DoesNotExist:
                try:
                  valid_datetime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return self.STATUS_CHOICES[self.ERROR]
                self.create(seq_no=seq_no, timestamp=valid_datetime, node=node_id,
                            sensor=sensor_id, value=readings)
                status = self.STATUS_CHOICES[self.CREATED]
            return status
        else:
            return self.STATUS_CHOICES[self.ERROR]

    def parse_readings(self, readings):
        processed_readings = []
        prev_gps_reading = None
        prev_acc_reading = None
        current_tz = timezone.get_current_timezone()

        for reading in readings:
            if prev_reading is None:
                prev_reading = reading

            local = current_tz.normalize(reading.timestamp)

            temp_reading = {'timestamp' : local,
                            'seqno': reading.seq_no,
                            'sensor_modality': reading.sensor.modality,
                            'sensor_format': reading.sensor.data_format,
                            'value' : reading.value
            }
            processed_readings.append(temp_reading)
        return json.dumps(processed_readings, cls=DjangoJSONEncoder)

    def get_readings(self, source=None, destination=None):

        try:
            if source and destination:
                readings = self.parse_readings(self.model.objects.get())
            else:
                readings = self.parse_readings(self.model.objects.all())
        except self.model.DoesNotExist:
            readings = False

        return readings

