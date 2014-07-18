from django.conf.urls import patterns, include, url
from mydashboard.views import (
		HomeView,
		CertificatesView,
		ReadingsView,
		NodeNewView,
		new_node_api,
		register_node_api,
		get_master_key_api,
		get_node_key_api,
		node_api,
		GenerateKeys,
		get_OTA_key_api
	)


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="dashboard"),
    url(r'^node_api$', node_api, name='node_api'),
    url(r'^get_node_keys$', GenerateKeys.as_view(), name='get_keys'),
    url(r'^certificates$', CertificatesView.as_view(), name="certificates"),
    url(r'^readings$', ReadingsView.as_view(), name="readings"),
    url(r'^new/sensor$', NodeNewView.as_view(), name="sensor"),
    url(r'^api/sensor/(?P<node_id>\d+)/status$', register_node_api, name="api_sensor_status"),
    url(r'^api/sensor/(?P<node_id>\d+)/key$', get_node_key_api, name="api_sensor_key"),
    url(r'^api/sensor/(?P<node_id>\d+)/otakey$', get_OTA_key_api, name="api_ota_key"),
    url(r'^api/sensor/new$', new_node_api, name="api_sensor"),
    url(r'^api/deployment/(?P<deployment_id>\d+)/master_key$', get_master_key_api, name="api_master_key")
)