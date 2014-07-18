from django.contrib import admin
from .models import (
		Node,
		AppConfig,
		SensorMap,
		Sensor,
        Reading
		)
admin.site.register(Node)
admin.site.register(AppConfig)
admin.site.register(SensorMap)
admin.site.register(Sensor)
admin.site.register(Reading)
