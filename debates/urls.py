from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
	path('', TemplateView.as_view(template_name="debates.html")),
	path('create/', TemplateView.as_view(template_name="create_debate.html"), name="create_debate")
]