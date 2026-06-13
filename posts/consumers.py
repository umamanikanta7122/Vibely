import json

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async

from django.contrib.auth.models import User

from .models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        print("CONNECTED:", self.channel_name)

        self.room_name = self.scope[
            'url_route'
        ]['kwargs']['room_name']

        self.room_group_name = self.room_name

        print("ROOM:", self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):

        print("DISCONNECTED")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    @sync_to_async
    def save_message(
        self,
        sender_username,
        receiver_username,
        message
    ):

        sender = User.objects.get(
            username=sender_username
        )

        receiver = User.objects.get(
            username=receiver_username
        )

        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )


    async def receive(self, text_data):

        print("MESSAGE RECEIVED")

        data = json.loads(text_data)

        message = data["message"]
        sender = data["sender"]
        receiver = data["receiver"]


        # SAVE IN DATABASE
        await self.save_message(
            sender,
            receiver,
            message
        )


        # SEND TO GROUP
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender
            }
        )


    async def chat_message(self, event):

        print("BROADCASTING")

        message = event["message"]
        sender = event["sender"]

        await self.send(
            text_data=json.dumps({

                "message": message,

                "sender": sender

            })
        )