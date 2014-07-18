# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SensorMap.modality_bit'
        db.add_column('actors_sensormap', 'modality_bit',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SensorMap.modality_bit'
        db.delete_column('actors_sensormap', 'modality_bit')


    models = {
        'actors.appconfig': {
            'Meta': {'object_name': 'AppConfig'},
            'config_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'actors.node': {
            'Meta': {'object_name': 'Node'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'node'", 'to': "orm['actors.AppConfig']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'node_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'actors.reading': {
            'Meta': {'object_name': 'Reading'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensor_reading'", 'to': "orm['actors.Node']"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensor_reading'", 'to': "orm['actors.Sensor']"}),
            'seq_no': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 18, 0, 0)'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'actors.sensor': {
            'Meta': {'object_name': 'Sensor'},
            'data_format': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modality': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'actors.sensormap': {
            'Meta': {'object_name': 'SensorMap'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensor_map'", 'to': "orm['actors.AppConfig']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modality_bit': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensor_map'", 'to': "orm['actors.Sensor']"})
        }
    }

    complete_apps = ['actors']