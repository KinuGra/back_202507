from django.core.management.base import BaseCommand
from main.models import QuizData1, Room, User
import uuid

class Command(BaseCommand):
    help = 'Create test data for quiz application'

    def handle(self, *args, **options):
        # Create test quiz questions
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