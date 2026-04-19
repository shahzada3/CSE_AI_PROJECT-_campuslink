import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from accounts.models import User


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        user_ids = sorted([str(self.user.id), str(self.receiver_id)])
        self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        if not message:
            return

        user = self.scope["user"]

        # Save message to database
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": user.id,
                "username": user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "username": event["username"],
        }))

    @database_sync_to_async
    def save_message(self, content):
        try:
            receiver = User.objects.get(id=self.receiver_id)
            Message.objects.create(
                sender=self.scope["user"],
                receiver=receiver,
                content=content
            )
        except User.DoesNotExist:
            pass
