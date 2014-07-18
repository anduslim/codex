from django.conf.urls import patterns, include, url
from mydashboard.views import (
		HomeView,
		ReadingsView,
		new_node_api,
        post_readings_api
	)


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="dashboard"),
    url(r'^readings$', ReadingsView.as_view(), name="readings"),
    url(r'^api/sensor/new$', new_node_api, name="api_sensor"),
    url(r'^api/sensor/(?P<node_id>\d+)/readings$', post_readings_api, name="post_sensor_readings"),
)
