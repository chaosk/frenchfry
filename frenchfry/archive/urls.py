# urls.py
from django.conf.urls.defaults import *
from tastypie.api import Api
from archive.api.resources import GameResource, GameStatResource

v1_api = Api(api_name='v1')
v1_api.register(GameResource())
v1_api.register(GameStatResource())

urlpatterns = patterns('',
	(r'^api/', include(v1_api.urls)),
)