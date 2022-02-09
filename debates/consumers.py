import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from debates.models import Debate


class DebateConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		debate_public_id = self.scope["url_route"]["kwargs"]["uuid"]

		if not await self.check_if_debate_exists(debate_public_id):
			await self.close(code=404)

		await self.channel_layer.group_add("debate", self.channel_name)
		await self.accept()

	async def disconnect(self, code):
		await self.channel_layer.group_discard("debate", self.channel_name)

	async def receive_json(self, content, **kwargs):
		pass

	@database_sync_to_async
	def check_if_debate_exists(self, public_id):
		return Debate.objects.filter(public_id=public_id).exists()



