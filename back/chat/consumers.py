import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from .models import Message
from financeApp.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        user = self.scope['user']
        await self.update_user_status(user, True)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        user = self.scope['user']
        await self.update_user_status(user, False)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        user_id = data['user_id']
        room = data['room']

        await self.save_message(user_id, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'user_id': user_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, user_id, room, message):
        user = CustomUser.objects.get(id=user_id)
        Message.objects.create(user=user, room=room, content=message)

    @database_sync_to_async
    def update_user_status(self, user, status):
        return CustomUser.objects.filter(pk=user.pk).update(is_online=status)


class GetInfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'info'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_info(self, event):
        await self.send(text_data=json.dumps(event))
