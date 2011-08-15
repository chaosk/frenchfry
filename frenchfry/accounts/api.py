from django.contrib.auth.models import User
from tastypie.authorization import Authorization


class UserResource(ModelResource):

	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		authorization = Authorization()
		allowed_methods = ['get']

	# TODO add api_key retrieving
