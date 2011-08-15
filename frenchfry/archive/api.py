from django.conf.urls.defaults import url
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.validation import FormValidation
from accounts.api import UserResource
from archive.models import Game, GameStat, Screenshot, ClientDemo
from archive.forms import ApiGameForm, ApiGameStatForm
from archive.utils import Base64FileField


class PostAuthentication(ApiKeyAuthentication):
	def is_authenticated(self, request, **kwargs):
		if request.method == "GET":
			return True
		return super(PostAuthentication, self) \
			.is_authenticated(request, **kwargs)


class GameResource(ModelResource):
	created_by = fields.ForeignKey(UserResource, 'created_by')

	class Meta:
		queryset = Game.objects.all()
		resource_name = 'game'
		authentication = PostAuthentication()
		authorization = Authorization()
		allowed_methods = ['get', 'post']
		validation = FormValidation(form_class=ApiGameForm)

	def override_urls(self):
		return [
			url(r"^(?P<resource_name>{0})/check{1}$".format(
				self._meta.resource_name, trailing_slash()),
				self.wrap_view('get_check'), name="api_get_check"),
		]

	def get_search(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		self.is_authenticated(request)
		self.throttle_check(request)

		try:
			game = Game.objects.get(game_id=request.GET.get('game_id', ''))
		except Game.DoesNotExist:
			raise Http404("Sorry, no game matching this ID.")

		context = {
			'id': game.id,
			'has_stats': game.has_all_stats(),
			'has_scoreboard': game.has_scoreboard(),
			'has_statboard': game.has_statboard(),
		}

		return self.create_response(request, context)

	def obj_create(self, bundle, request=None, **kwargs):
		return super(GameResource, self).obj_create(bundle,
			request, created_by=request.user)


class GameStatResource(ModelResource):

	class Meta:
		queryset = GameStat.objects.all()
		resource_name = 'gamestat'
		authentication = PostAuthentication()
		authorization = Authorization()
		allowed_methods = ['post']
		validation = FormValidation(form_class=ApiGameStatForm)

	def obj_create(self, bundle, request=None, **kwargs):
		return super(GameStatResource, self).obj_create(bundle,
			request, user=request.user)


class ScreenshotResource(ModelResource):
	sent_by = fields.ForeignKey(UserResource, 'sent_by')
	screenshot_file = Base64FileField('screenshot_file')

	class Meta:
		queryset = Screenshot.objects.all()
		resource_name = 'screenshot'
		authentication = PostAuthentication()
		authorization = Authorization()
		allowed_methods = ['post']

	def obj_create(self, bundle, request=None, **kwargs):
		return super(ScreenshotResource, self).obj_create(bundle,
			request, sent_by=request.user)


class ClientDemoResource(ModelResource):
	sent_by = fields.ForeignKey(UserResource, 'sent_by')
	demo_file = Base64FileField('demo_file')

	class Meta:
		queryset = ClientDemo.objects.all()
		resource_name = 'clientdemo'
		authentication = PostAuthentication()
		authorization = Authorization()
		allowed_methods = ['post']

	def obj_create(self, bundle, request=None, **kwargs):
		return super(ClientDemoResource, self).obj_create(bundle,
			request, sent_by=request.user)
