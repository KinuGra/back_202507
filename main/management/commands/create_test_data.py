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
                'question': '夏の大三角とは、こと座のベガ、わし座のアルタイル、はくちょう座の何？',
                'answer_full': 'デネブ',
                'answer_letters': ['で', 'ね', 'ぶ'],
                'category': 'Japanese'
            },
            {
                'questionId': 1,
                'quizId': 1,
                'question': '「夏草や 兵どもが 夢の中」という句を読んだ俳人は誰？',
                'answer_full': '松尾芭蕉',
                'answer_letters': ['ま', 'つ', 'お', 'ば', 'し', 'ょ', 'う'],
                'category': 'Japanese'
            },
            {
                'questionId': 2,
                'quizId': 1,
                'question': '毎年7月に行われ、京の三大祭の一つとしても知られる祭は何？',
                'answer_full': '祇園祭',
                'answer_letters': ['ぎ', 'お', 'ん', 'ま', 'つ', 'り'],
                'category': 'Japanese'
            },
            {
                'questionId': 3,
                'quizId': 1,
                'question': '13年周期や17年周期など周期的に大量発生するセミのことを、その周期の特徴から何と呼ぶ？',
                'answer_full': '素数ゼミ',
                'answer_letters': ['そ', 'す', 'う', 'ぜ', 'み'],
                'category': 'Japanese'
            },
            {
                'questionId': 4,
                'quizId': 1,
                'question': 'テングサという海藻を煮て作られ、漢字では「心太」と書かれるゼリー状の食品は何？',
                'answer_full': 'ところてん',
                'answer_letters': ['と', 'こ', 'ろ', 'て', 'ん'],
                'category': 'Japanese'
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