import datetime
from fastzap.models import Chat, Message
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        if self.scope['user'] is not None:
            chat = await self.get_chat(self.chat_id)
            if await self.is_user_on_chat(self.scope['user'], chat):
                await self.channel_layer.group_add(
                    self.chat_id,
                    self.channel_name
                )
                return await self.accept()
        return await self.close()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_id, self.channel_name)
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
    

    @database_sync_to_async
    def is_user_on_chat(self, user, chat):
        return user in chat.participants.all()

    @database_sync_to_async
    def get_chat(self, chat_id):
        return Chat.objects.get(pk=chat_id)
    
    @database_sync_to_async
    def save_message(self, message):
        Message.objects.create(text_content=message, sender=self.scope['user'], timestamp=datetime.datetime.now(), chat=Chat.objects.get(pk=self.chat_id))

    async def add_message(self, event):
        message = event['text_content']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'type': 'message_added',
            'data': {
                'text_content': message,
                'sender': sender
            }
            
        }, ensure_ascii=False))
