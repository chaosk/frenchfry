from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class LoginRequiredMiddleware(object):

	def process_request(self, request):
		path = request.path
		url = reverse('home')
		if request.user.is_authenticated() or path == url \
			or path.startswith(('/media', '/__',)):
			return
		return HttpResponseRedirect(url)
