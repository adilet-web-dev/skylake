from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path
from debates.api.views import DebateViewSet , SearchWithCandidateView,SearchDebateView, SearchDebateFullView



if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("debates", DebateViewSet)

app_name = "api"

urlpatterns=[
    path("debates/search/<str:topic>", SearchDebateView.as_view()),
    path("debates/search_c/<str:candidate>", SearchWithCandidateView.as_view()),
    path("debates/search/<str:candidate>/<str:topic>",SearchDebateFullView.as_view()),
]
urlpatterns+=router.urls

