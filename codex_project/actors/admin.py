from django.contrib import admin
from .models import (
		Node,
		AppConfig,
		SensorMap,
		Sensor
		)
admin.site.register(Node)
admin.site.register(AppConfig)
admin.site.register(SensorMap)
admin.site.register(Sensor)