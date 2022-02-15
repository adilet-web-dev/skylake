from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('ws/debates/<int:id>/<str:session_key>/', consumers.DebateConsumer.as_asgi(), name='debates')
]
