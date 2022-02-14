from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('ws/debates/<int:id>/', consumers.DebateConsumer.as_asgi(), name='debates')
]
