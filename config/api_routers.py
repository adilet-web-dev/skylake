from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from debates.api.views import DebateViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("debates", DebateViewSet)

app_name = "api"
urlpatterns = router.urls

