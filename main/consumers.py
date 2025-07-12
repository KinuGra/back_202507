import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, QuizData1
from .serializers import RoomSerializer, QuizData1Serializer

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'room_{self.room_id}'

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

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        if message_type == 'get_room_data':
            room_data = await self.get_room_data()
            await self.send(text_data=json.dumps({
                'type': 'room_data',
                'data': room_data
            }))

        elif message_type == 'get_answer_data':
            quiz_id = data['quiz_id']
            answer_data = await self.get_answer_data(quiz_id)
            await self.send(text_data=json.dumps({
                'type': 'answer_data',
                'data': answer_data
            }))

    @database_sync_to_async
    def get_room_data(self):
        try:
            room = Room.objects.get(roomId=self.room_id)
            return RoomSerializer(room).data
        except Room.DoesNotExist:
            return None

    @database_sync_to_async
    def get_answer_data(self, quiz_id):
        answers = QuizData1.objects.filter(quizId=quiz_id)
        return QuizData1Serializer(answers, many=True).data

    async def room_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'room_update',
            'data': event['data']
        }))