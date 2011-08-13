from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('accounts.views',
	url(r'^login/$', 'login', name='login'),
	url(r'^logout/$', 'logout', name='logout'),
	url(r'^new/$', 'add_user', name='add_user'),
	url(r'^list/$', 'userlist', name='userlist'),
	url(r'^profile/(?P<user_id>[-\d]+)/$', 'profile', name='profile'),
)
