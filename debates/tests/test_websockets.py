from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from voting.models import Vote

from django.test import TransactionTestCase
from debates.api.serializers import CandidateSerializer
from django.db.models import Model

from users.factories import UserFactory
from debates.factories import DebateFactory, CandidateFactory
from debates.routing import websocket_urlpatterns
from debates.events import EVENTS


application = URLRouter(websocket_urlpatterns)


class TestDebateConsumer(TransactionTestCase):
	def setUp(self) -> None:
		self.user = UserFactory()
		self.debate = DebateFactory()

	async def test_it_creates_connection(self):
		communicator = WebsocketCommunicator(
			application,
			f'/ws/debates/{self.debate.id}/{self.user.private_id}/'
		)

		connected, _ = await communicator.connect()
		self.assertTrue(connected)
		await communicator.disconnect()

	async def test_it_votes_candidate(self):
		# implementation is working, but test doesn't
		# TODO write later
		candidate = await self.get_candidate(self.debate)
		communicator = WebsocketCommunicator(
			application,
			f'/ws/debates/{self.debate.id}/{self.user.private_id}/'
		)

		await communicator.connect()

		await communicator.send_json_to(
			{
				"event": EVENTS['VOTE'],
				"candidate": CandidateSerializer(instance=candidate).data,
				"score": 1
			}
		)


	@database_sync_to_async
	def create_user(self):
		return UserFactory()

	@database_sync_to_async
	def create_debate(self):
		return DebateFactory()

	@database_sync_to_async
	def get_candidate(self, debate: Model):
		return CandidateFactory.create(debate=debate)
