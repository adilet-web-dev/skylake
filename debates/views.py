from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def debate_view(request, pk):
	return render(request, "debates.html", {"id": pk})
