from django.urls import path
from django.views.generic import TemplateView

from .views import debate_view, DebateListView, MyDebateListView, CreateDebateTemplateView

urlpatterns = [
	path('<int:pk>/', debate_view, name='debate'),
	path('create/', CreateDebateTemplateView.as_view(), name="create_debate"),
	path('', DebateListView.as_view(), name="debate_list"),
	path('my-debates/', MyDebateListView.as_view(), name="my_debate_list")
]