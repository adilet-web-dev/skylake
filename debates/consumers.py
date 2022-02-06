import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DebateConsumer(AsyncJsonWebsocketConsumer):
	def __init__(self):
		self.biden = 0
		self.trump = 0
		super(DebateConsumer, self).__init__()

	async def connect(self):
		self.room_name = 'debate1'

		await self.channel_layer.group_add(
			self.room_name,
			self.channel_name
		)

		await self.accept()

	async def receive_json(self, content, **kwargs):
		await self.channel_layer.group_send(
			self.room_name,
			{
				"type": "send_message",
				"message": content
			}
		)

	async def send_message(self, event):
		await self.send_json(event["message"])
