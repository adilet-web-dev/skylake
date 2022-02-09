from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('ws/debates/<uuid:uuid>/', consumers.DebateConsumer.as_asgi(), name='debates')
]
