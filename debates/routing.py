from django.urls import path

from .websockets import consumers

websocket_urlpatterns = [
	path('ws/debates/<int:id>/<uuid:private_id>/', consumers.DebateConsumer.as_asgi(), name='debates')
]
