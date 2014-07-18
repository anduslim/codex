# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table('actors_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('node_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('app_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actors.AppConfig'], related_name='node')),
        ))
        db.send_create_signal('actors', ['Node'])

        # Adding model 'AppConfig'
        db.create_table('actors_appconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('config_id', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('actors', ['AppConfig'])

        # Adding model 'SensorMap'
        db.create_table('actors_sensormap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modality_bit', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('app_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actors.AppConfig'], related_name='sensor_map')),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actors.Sensor'], related_name='sensor_map')),
        ))
        db.send_create_signal('actors', ['SensorMap'])

        # Adding model 'Sensor'
        db.create_table('actors_sensor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modality', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('data_format', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('actors', ['Sensor'])

        # Adding model 'Reading'
        db.create_table('actors_reading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seq_no', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 18, 0, 0))),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actors.Node'], related_name='sensor_reading')),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actors.Sensor'], related_name='sensor_reading')),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('actors', ['Reading'])


    def backwards(self, orm):
        # Deleting model 'Node'
        db.delete_table('actors_node')

        # Deleting model 'AppConfig'
        db.delete_table('actors_appconfig')

        # Deleting model 'SensorMap'
        db.delete_table('actors_sensormap')

        # Deleting model 'Sensor'
        db.delete_table('actors_sensor')

        # Deleting model 'Reading'
        db.delete_table('actors_reading')


    models = {
        'actors.appconfig': {
            'Meta': {'object_name': 'AppConfig'},
            'config_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'actors.node': {
            'Meta': {'object_name': 'Node'},
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['actors.AppConfig']", 'related_name': "'node'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'node_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'actors.reading': {
            'Meta': {'object_name': 'Reading'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['actors.Node']", 'related_name': "'sensor_reading'"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['actors.Sensor']", 'related_name': "'sensor_reading'"}),
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
            'app_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['actors.AppConfig']", 'related_name': "'sensor_map'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modality_bit': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['actors.Sensor']", 'related_name': "'sensor_map'"})
        }
    }

    complete_apps = ['actors']