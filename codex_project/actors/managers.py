from django.db import models

class NodesManager(models.Manager):

	def create_node(self, _deployment, _node_id, _node_type, _key_version, _AK, _EK, _GK, _OTAK, _app_config):

		try:
			node = self.model.objects.get()
		except self.model.DoesNotExist:

			node = self.create(node_id=_node_id, node_type=_node_type, app_config=_app_config)

		return node

class ReadingsManager(models.Manager):

    def add_reading(self, timestamp, seq_no, node_id, sensor_id, readings):

        try:
            reading = self.model.objects.get(seq_no=seq_no)
        except self.model.DoesNotExist:
            reading = self.create(seq_no=seq_no, timestamp=timestamp, node=node_id,
                        sensor=sensor_id, value=readings)
        return reading

