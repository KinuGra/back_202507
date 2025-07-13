from django.core.management.base import BaseCommand
from main.models import QuizData1, Room, User, RoomParticipants
import uuid
import json

class Command(BaseCommand):
    help = 'Create test data for quiz application'

    def handle(self, *args, **options):
        # Create test quiz questions (日本語クイズ)
        test_questions = [
            {
                'questionId': 0,
                'quizId': 1,
                'question': '日本で一番高い山は？',
                'answer_full': 'ふじさん',
                'answer_letters': json.dumps(['ふ', 'じ', 'さ', 'ん']),
                'category': '地理'
            },
            {
                'questionId': 1,
                'quizId': 1,
                'question': '日本の国鳥は？',
                'answer_full': 'きじ',
                'answer_letters': json.dumps(['き', 'じ']),
                'category': '自然'
            },
            {
                'questionId': 2,
                'quizId': 1,
                'question': '東京都の花は？',
                'answer_full': 'そめいよしの',
                'answer_letters': json.dumps(['そ', 'め', 'い', 'よ', 'し', 'の']),
                'category': '地理'
            },
            {
                'questionId': 3,
                'quizId': 1,
                'question': '猫を英語で何と言いますか？',
                'answer_full': 'cat',
                'answer_letters': json.dumps(['c', 'a', 't']),
                'category': '英語'
            },
            {
                'questionId': 4,
                'quizId': 1,
                'question': '水を日本語で何と言いますか？',
                'answer_full': 'みず',
                'answer_letters': json.dumps(['み', 'ず']),
                'category': '日本語'
            }
        ]

        for q_data in test_questions:
            quiz, created = QuizData1.objects.get_or_create(
                questionId=q_data['questionId'],
                defaults=q_data
            )
            if created:
                self.stdout.write(f'Created question: {quiz.question}')

        # Create test users
        test_users = [
            {
                'uuid': '550e8400-e29b-41d4-a716-446655440000',
                'username': '田中太郎',
                'icon': '/images/avatars/person_avatar_1.png',
                'loginId': 'tanaka123',
                'password': 'hashed_password'
            },
            {
                'uuid': '550e8400-e29b-41d4-a716-446655440001',
                'username': '佐藤花子',
                'icon': '/images/avatars/person_avatar_2.png',
                'loginId': 'sato456',
                'password': 'hashed_password'
            },
            {
                'uuid': '550e8400-e29b-41d4-a716-446655440002',
                'username': '鈴木一郎',
                'icon': '/images/avatars/person_avatar_3.png',
                'loginId': 'suzuki789',
                'password': 'hashed_password'
            },
            {
                'uuid': 'test-user-uuid',
                'username': 'Test User',
                'icon': '/images/avatars/person_avatar_4.png',
                'loginId': 'test-user',
                'password': 'default'
            }
        ]

        for user_data in test_users:
            user, created = User.objects.get_or_create(
                loginId=user_data['loginId'],
                defaults=user_data
            )
            if created:
                self.stdout.write(f'Created user: {user.username} ({user.uuid})')
            else:
                self.stdout.write(f'User already exists: {user.username} ({user.loginId})')

        # Create test rooms
        test_rooms = [
            {
                'roomId': 'test-room',
                'status': 'waiting',
                'currentSeq': 0,
                'quizId': 1
            },
            {
                'roomId': 'ABCD1234',
                'status': 'waiting',
                'currentSeq': 0,
                'quizId': 1
            }
        ]

        for room_data in test_rooms:
            room, created = Room.objects.get_or_create(
                roomId=room_data['roomId'],
                defaults=room_data
            )
            if created:
                self.stdout.write(f'Created room: {room.roomId}')

        # Create test room participants
        test_room = Room.objects.get(roomId='test-room')
        test_user = User.objects.get(uuid='test-user-uuid')
        
        participant, created = RoomParticipants.objects.get_or_create(
            roomId=test_room.id,
            uuid=test_user.uuid,
            defaults={'currentScore': 0}
        )
        if created:
            self.stdout.write(f'Added participant: {test_user.username} to {test_room.roomId}')

        self.stdout.write(self.style.SUCCESS('Test data created successfully!'))
        self.stdout.write('\n=== Created Data Summary ===')
        self.stdout.write(f'Questions: {QuizData1.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Rooms: {Room.objects.count()}')
        self.stdout.write(f'Participants: {RoomParticipants.objects.count()}')