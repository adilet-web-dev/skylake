import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from voting.models import Vote

from debates.events import EVENTS
from debates.models import Debate, Candidate
from debates.utils import get_user


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
		session_key = self.scope["url_route"]["kwargs"]["session_key"]
		self.user = await get_user(session_key)
		if not await self.is_authenticated(self.user):
			await self.disconnect(code=403)

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

	@database_sync_to_async
	def is_authenticated(self, user):
		return user.is_authenticated


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
			await self.add_vote_to_candidate(
				candidate=content["candidate"]["name"],
				user=self.user,
				score=content["score"]
			)

			await self.channel_layer.group_send(
				self.group_name, {
					"type": "update_votes",
					"candidate": content["candidate"]["name"],
					"score": await self.get_total_votes(content["candidate"]["name"])
				}
			)

	async def update_online_users_number(self, event):
		await self.send(text_data=json.dumps({
			"event": EVENTS["UPDATE_ONLINE_USERS_NUMBER"],
			"count": await self.get_channels_number()
		}))

	async def update_votes(self, event):
		await self.send(text_data=json.dumps({
			"event": EVENTS["UPDATE_VOTES"],
			**event
		}))

	@database_sync_to_async
	def add_vote_to_candidate(self, candidate, user, score):
		debate = Debate.objects.get(id=self.debate_id)
		candidate = debate.candidates.get(name=candidate)

		vote = Vote.objects.get_for_user(candidate, user)
		Vote.objects.record_vote(candidate, user, score)

	@database_sync_to_async
	def get_total_votes(self, candidate):
		candidate = Candidate.objects.get(name=candidate)
		score = Vote.objects.get_score(candidate)["score"]
		return score
