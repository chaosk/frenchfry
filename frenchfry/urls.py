from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from tastypie.api import Api
from accounts.api import UserResource
from archive.api import GameResource, GameStatResource
from archive.api import ScreenshotResource, ClientDemoResource

v1_api = Api(api_name='v1')
v1_api.register(GameResource())
v1_api.register(GameStatResource())
v1_api.register(ScreenshotResource())
v1_api.register(ClientDemoResource())
v1_api.register(UserResource())


urlpatterns = patterns('',
	(r'^accounts/', include('accounts.urls')),
	(r'^api/', include(v1_api.urls)),
	url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
)

import settings
if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.MEDIA_ROOT,
			'show_indexes': True,
		}),
	)