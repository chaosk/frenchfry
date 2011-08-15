from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from archive.models import Match


def match_list(request):
	matches = Match.objects.order_by('-created_at')
	if not request.user.is_staff and not request.user.is_superuser:
		matches = matches.exclude(is_verified=False)
	return TemplateResponse(request, 'archive/list.html', {
		'matches': matches,
	})


def match_detail(request, match_id):
	# match = get_object_or_404(Match, pk=match_id)
	return TemplateResponse(request, 'archive/detail.html', {
		# 'match': match,
	})
