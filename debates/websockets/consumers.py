import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from debates.events import EVENTS
from debates.websockets.db import AsyncDatabase


channels = []


class ChannelsCounter:
	async def add_channel(self, channel_name):
		channels.append(channel_name)

	async def remove_channel(self, channel_name):
		channels.remove(channel_name)

	async def get_channels_number(self):
		return len(channels)


class BaseDebateConsumer(AsyncJsonWebsocketConsumer, AsyncDatabase):
	"""
	This class is responsible for base connection and disconnection events, authorization
	"""
	def __init__(self):
		self.user = None
		self.group_name = None
		self.debate_id = None
		super(BaseDebateConsumer, self).__init__()

	async def connect(self):
		await self.authenticate()
		await self.validate_debate()

		self.group_name = f"debate-{self.debate_id}"

		await self.channel_layer.group_add(self.group_name, self.channel_name)
		await self.accept()

	async def authenticate(self):
		private_id = self.scope["url_route"]["kwargs"]["private_id"]
		user = await self.get_user_or_none(private_id)
		if not user:
			await self.disconnect(403)
		else:
			self.user = user

	async def validate_debate(self):
		self.debate_id = self.scope["url_route"]["kwargs"]["id"]
		if not await self.check_if_debate_exists(self.debate_id):
			await self.close(code=404)

	async def disconnect(self, code=None):
		await self.channel_layer.group_discard("debate", self.channel_name)


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
				score=content["score"],
				debate_id=self.debate_id
			)

			await self.channel_layer.group_send(
				self.group_name, {
					"type": "update_votes",
					"candidate": content["candidate"]["name"],
					"score": await self.get_total_votes(content["candidate"]["name"])
				}
			)

		if content["event"] == EVENTS["COMMENT"]:
			await self.create_comment(
				comment=content["comment"],
				user=self.user,
				debate_id=self.debate_id
			)

			await self.channel_layer.group_send(
				self.group_name, {
					"type": "send_comment",
					"comment": content["comment"],
					"user": self.user.username
				}
			)

	async def update_online_users_number(self, event):
		await self.send(text_data=json.dumps({
			"event": EVENTS["UPDATE_ONLINE_USERS_NUMBER"],
			"count": await self.get_channels_number()
		}))

	async def send_comment(self, event):
		await self.send(text_data=json.dumps({
			"event": EVENTS["COMMENT"],
			**event
		}))

	async def update_votes(self, event):
		await self.send(text_data=json.dumps({
			"event": EVENTS["UPDATE_VOTES"],
			**event
		}))
