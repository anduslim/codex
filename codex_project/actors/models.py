
from django.db import models
from . import managers
from django.utils import timezone


class Node(models.Model):
    ''' node information
    '''
    SENSOR_NODE, GATEWAY_NODE, SNIFFER_NODE = range(3)
    NODES_CHOICES = (
            (SENSOR_NODE, u'Sensor'),
            (GATEWAY_NODE, u'Gateway'),
            (SNIFFER_NODE, u'Sniffer')
        )

    node_id = models.PositiveIntegerField(blank=False)

    node_type = models.PositiveSmallIntegerField(
            default=SENSOR_NODE,
            choices=NODES_CHOICES
            )

    app_config = models.ForeignKey('AppConfig', blank=False, null=False,
                        related_name='node')

    objects = managers.NodesManager()

    def __str__(self):
        return ', '.join([str(self.id), str(self.node_id), self.get_node_type_display()])


class AppConfig(models.Model):
    '''AppConfig information
    '''
    config_id = models.PositiveSmallIntegerField()

    def __str__(self):
        return ', '.join([str(self.id)])


class SensorMap(models.Model):
    ''' Sensor mapping information
    '''

    modality_bit = models.PositiveSmallIntegerField()

    app_config = models.ForeignKey('AppConfig', blank=False, null=False,
                        related_name='sensor_map')

    sensor = models.ForeignKey('Sensor', blank=False, null=False,
                        related_name='sensor_map')

    def __str__(self):
        return ', '.join([str(self.id), 'config_id-' +
            str(self.app_config_id), 'bit-' +
            str(self.modality_bit), self.sensor.modality])


class Sensor(models.Model):
    ''' Sensor information
    '''

    modality = models.CharField(max_length=50)

    data_format = models.CharField(max_length=100)

    def __str__(self):
        return ', '.join([str(self.id), self.modality])


class Reading(models.Model):
    ''' Sensor Readings
    '''
    seq_no = models.PositiveIntegerField()

    timestamp = models.DateTimeField(default=timezone.now())

    node = models.ForeignKey('Node', blank=False, null=False,
                        related_name='sensor_reading')

    sensor = models.ForeignKey('Sensor', blank=False, null=False,
                        related_name='sensor_reading')

    value = models.CharField(max_length=100)

    objects = managers.ReadingsManager()

    def __str__(self):
        return ', '.join([str(self.id), str(self.timestamp), 'node ' + str(self.node.node_id),
            self.sensor.modality, self.value])

