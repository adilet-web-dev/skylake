from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.test import TransactionTestCase

from users.factories import UserFactory
from debates.factories import DebateFactory
from debates.websockets.consumers import DebateConsumer


class TestDebateConsumer(TransactionTestCase):
	async def test_it_creates_connection(self):
		user = await self.create_user()
		debate = await self.create_debate()

		communicator = WebsocketCommunicator(
			DebateConsumer.as_asgi(),
			f'ws/debates/{debate.id}/<str:session_key>/'
		)

		await communicator.connect()

	@database_sync_to_async
	def create_user(self):
		return UserFactory()

	@database_sync_to_async
	def create_debate(self):
		return DebateFactory()
