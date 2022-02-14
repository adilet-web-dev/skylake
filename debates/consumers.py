import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from debates.events import EVENTS
from debates.models import Debate


channels = []


class ChannelsCounter:
	async def add_channel(self, channel_name):
		channels.append(channel_name)

	async def remove_channel(self, channel_name):
		channels.remove(channel_name)

	async def get_channels_number(self):
		return len(channels)


class BaseDebateConsumer(AsyncJsonWebsocketConsumer):
	"""
	This class is responsible for base connection and disconnection events
	"""
	async def connect(self):
		self.debate_id = self.scope["url_route"]["kwargs"]["id"]

		if not await self.check_if_debate_exists(self.debate_id):
			await self.close(code=404)

		self.group_name = f"debate-{self.debate_id}"

		await self.channel_layer.group_add(self.group_name, self.channel_name)
		await self.accept()

	async def disconnect(self, code=None):
		await self.channel_layer.group_discard("debate", self.channel_name)

	@database_sync_to_async
	def check_if_debate_exists(self, debate_id):
		return Debate.objects.filter(id=debate_id).exists()


class DebateConsumer(BaseDebateConsumer, ChannelsCounter):
	async def connect(self):
		await super(DebateConsumer, self).connect()
		await self.add_channel(self.channel_name)

		await self.channel_layer.group_send(
			self.group_name, {"type": "update_online_users_number"}
		)

	async def disconnect(self, code=None):
		channel_name = self.channel_name
		await super(DebateConsumer, self).disconnect()
		await self.remove_channel(channel_name)
		await self.channel_layer.group_send(
			self.group_name, {"type": "update_online_users_number"}
		)

	async def receive_json(self, content, **kwargs):
		if content["event"] == EVENTS["VOTE"]:
			await self.add_vote_to_candidate(content["candidate"]["name"])

	async def update_online_users_number(self, event):
		await self.send(text_data=json.dumps({
			"event": EVENTS["UPDATE_ONLINE_USERS_NUMBER"],
			"count": await self.get_channels_number()
		}))

	@database_sync_to_async
	def add_vote_to_candidate(self, candidate):
		debate = Debate.objects.get(id=self.debate_id)
		candidate = debate.candidates.get(name=candidate)
		candidate.votes += 1
		candidate.save()
