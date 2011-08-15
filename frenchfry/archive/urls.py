# urls.py
from django.conf.urls.defaults import *

urlpatterns = patterns('archive.views',
	url(r'^list/$', 'match_list', name='match_list'),
	url(r'^match/(?P<match_id>\d+)/$', 'match_detail', name='match_detail'),
)
