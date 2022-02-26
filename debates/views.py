from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse

from debates.models import Debate


@login_required
def debate_view(request, pk):
	return render(request, "debates.html", {"id": pk})

class CreateDebateTemplateView(LoginRequiredMixin, TemplateView):
	template_name = "create_debate.html"


class DebateListView(ListView):
	model = Debate
	template_name = "debate_list.html"
	context_object_name = "debates"


class MyDebateListView(LoginRequiredMixin, ListView):
	model = Debate
	template_name = "debate_list.html"
	context_object_name = "debates"

	def get_queryset(self):
		user = self.request.user
		return user.debates.all()
