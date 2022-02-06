from django.test import TestCase
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from debates.routing import websocket_urlpatterns


application = URLRouter(websocket_urlpatterns)


class TestDebateConsumer(TestCase):
	async def test_it_creates_connection(self):
		communicator = WebsocketCommunicator(application, "/ws/debate/")
		connected, _ = await communicator.connect()
		self.assertTrue(connected)
		await communicator.disconnect()

	async def test_it_sends_message_when_joined(self):
		communicator = WebsocketCommunicator(application, "/ws/debate/")
		await communicator.connect()
		await communicator.send_json_to("hello")

		response = await communicator.receive_json_from()
		self.assertEqual(response, "hello")

