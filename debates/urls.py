from django.urls import path
from django.views.generic import TemplateView

from .views import debate_view, DebateListView

urlpatterns = [
	path('<int:pk>/', debate_view, name='debate'),
	path('create/', TemplateView.as_view(template_name="create_debate.html"), name="create_debate"),
	path('', DebateListView.as_view(), name="debate_list")
]