from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from debates.models import Debate


@login_required
def debate_view(request, pk):
	return render(request, "debates.html", {"id": pk})


class DebateListView(ListView):
	model = Debate
	template_name = "debate_list.html"
	context_object_name = "debates"
