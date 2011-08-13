from django.conf.urls.defaults import *
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^accounts/', include('accounts.urls')),
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