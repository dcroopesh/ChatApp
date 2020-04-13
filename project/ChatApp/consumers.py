import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import chatapp,room,p2p
from django.contrib.auth.models import User
from django.db.models import Q

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        #print(self.channel_name)
        
        await self.accept()
        await self.db_to_socket()

    @database_sync_to_async
    def addToDB(self,username,message,roomname):
        user = User.objects.get(username=username)
        chat = chatapp.objects.create(username=user,message=message,roomname=roomname)
        chat.save()

    @database_sync_to_async
    def get_message_from_db(self,roomname):
        chat = chatapp.objects.filter(roomname=roomname)
        messages = []
        for each in chat:
            messages.append((each.username,each.message))

        return messages

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.addToDB(self.user,message,self.room_name)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {        
                "type": "chat.message",
                "username":str(self.user),
                "message": message ,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        
        await self.send(text_data=json.dumps({
            "username": str(self.user) ,
            "message": message

        }))

    async def db_to_socket(self):    
        messages = await self.get_message_from_db(self.room_name)
        for message in messages:
            await self.send(text_data=json.dumps({
                    "username": str(message[0]) ,
                    "message": message[1]

                }))


class P2P(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        database_sync_to_async(room.objects.create(user=self.user))
        self.receiver = await self.get_receiver(self.user)
        await self.accept()     
        await self.db_to_socket()

    @database_sync_to_async
    def get_receiver(self,userr):
        return room.objects.filter(~Q(user=userr))[0].user

    @database_sync_to_async
    def addToDB(self,username,message,receiver):

        user1 = User.objects.get(username=username)
        user2 = User.objects.get(username=receiver)
        chat = p2p.objects.create(username=user1,message=message,roomname=self.room_name,receiver=user2)
        chat.save()

    @database_sync_to_async
    def get_message_from_db(self,username,receiver):
        user1 = User.objects.get(username=username)
        user2 = User.objects.get(username=receiver)
        chat = p2p.objects.filter((Q(username=user1) & Q(receiver=user2)) | (Q(username=user2) & Q(receiver=user1)))
        
        messages = []
        for each in chat:
            messages.append((each.username,each.message))
        return messages

    async def disconnect(self, close_code):
        
        room.objects.all().delete()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        

        await self.addToDB(self.user,message,self.receiver)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "username":str(self.user),
                "message": message ,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['username']
        await self.send(text_data=json.dumps({
            "username": sender,
            "message": message

        }))

    async def db_to_socket(self):    
        messages = await self.get_message_from_db(self.user,self.receiver)
        
        for message in messages:
            sender = str(message[0])
            await self.send(text_data=json.dumps({
                    "username": sender,
                    "message": message[1]

                }))

