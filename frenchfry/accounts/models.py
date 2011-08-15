from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from tastypie.models import create_api_key


class UserProfile(models.Model):
	user = models.OneToOneField(User, unique=True, related_name='profile')

	def __unicode__(self):
		possessive = '' if self.user.username.endswith('s') else 's'
		return u"{0}'{1} profile".format(self.user.username, possessive)

	def get_absolute_url(self):
		return self.user.get_absolute_url()


def post_user_save(instance, **kwargs):
	if kwargs['created'] and instance.id > 0:
		UserProfile.objects.create(user=instance)

post_save.connect(post_user_save, sender=User,
	dispatch_uid='accounts.models')
post_save.connect(create_api_key, sender=User)
