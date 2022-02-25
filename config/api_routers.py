from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path
from debates.api.views import DebateViewSet , search_with_candidate_view,search_debate_view



if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("debates", DebateViewSet)

app_name = "api"

urlpatterns=[
    path("search/<str:topic>", search_debate_view.as_view()),
    path("search_c/<str:candidate>", search_with_candidate_view.as_view()),
]
urlpatterns+=router.urls

