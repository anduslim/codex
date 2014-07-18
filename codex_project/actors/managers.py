from django.db import models

class NodesManager(models.Manager):

	def create_node(self, _deployment, _node_id, _node_type, _key_version, _AK, _EK, _GK, _OTAK, _app_config):

		try:
			self.model.objects.get()
			node = None
		except self.model.DoesNotExist:

			node = self.create(node_id=_node_id, node_type=_node_type, app_config=_app_config)

		return node
