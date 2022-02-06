from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('ws/debate/', consumers.DebateConsumer.as_asgi(), name='debate')
]
