from django.core.management.base import BaseCommand
from main.models import QuizData1, Room, User
import uuid

class Command(BaseCommand):
    help = 'Create test data for quiz application'

    def handle(self, *args, **options):
        # Create test quiz questions
        test_questions = [
            {
                'questionId': 1,
                'quizId': 1,
                'question': 'What is the Japanese word for apple?',
                'answer_full': 'りんご',
                'answer_letters': ['り', 'ん', 'ご'],
                'category': 'Japanese'
            },
            {
                'questionId': 2,
                'quizId': 1,
                'question': 'What is the Japanese word for cat?',
                'answer_full': 'ねこ',
                'answer_letters': ['ね', 'こ'],
                'category': 'Japanese'
            },
            {
                'questionId': 3,
                'quizId': 1,
                'question': 'What is the Japanese word for water?',
                'answer_full': 'みず',
                'answer_letters': ['み', 'ず'],
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

        # Create test room
        test_room, created = Room.objects.get_or_create(
            roomId='test-room',
            defaults={
                'status': 'waiting',
                'currentSeq': 0,
                'quizId': 1
            }
        )
        if created:
            self.stdout.write(f'Created room: {test_room.roomId}')

        # Create test user
        test_user, created = User.objects.get_or_create(
            loginId='test-user',
            defaults={
                'username': 'Test User',
                'uuid': uuid.uuid4()
            }
        )
        if created:
            self.stdout.write(f'Created user: {test_user.username}')

        self.stdout.write(self.style.SUCCESS('Test data created successfully!'))