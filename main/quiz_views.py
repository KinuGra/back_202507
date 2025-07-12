from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
import random
from .models import Room, User, QuizData1, RoomParticipants, Answer
from .serializers import QuizData1Serializer

@csrf_exempt
@require_POST
def start_quiz_game(request):
    """クイズゲーム開始API"""
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        
        room = Room.objects.get(roomId=room_id)
        room.status = 'in_progress'
        room.currentSeq = 0
        room.save()
        
        # 最初の問題を取得
        quiz = QuizData1.objects.filter(quizId=room.quizId).first()
        
        return JsonResponse({
            'success': True,
            'question': QuizData1Serializer(quiz).data if quiz else None
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_POST
def submit_answer(request):
    """回答送信API"""
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        user_uuid = data.get('userUuid')
        answer = data.get('answer')
        
        room = Room.objects.get(roomId=room_id)
        user = User.objects.get(uuid=user_uuid)
        
        # 現在の問題を取得
        current_quiz = QuizData1.objects.filter(
            quizId=room.quizId,
            questionId=room.currentSeq
        ).first()
        
        is_correct = current_quiz and answer == current_quiz.answer_full
        
        # 回答を記録
        Answer.objects.create(
            roomPK_id=room,
            uuid=user,
            roomId=room,
            currentSeq=room.currentSeq,
            quizId=room.quizId,
            questionId=current_quiz.questionId if current_quiz else 0,
            isCorrect=is_correct
        )
        
        return JsonResponse({
            'success': True,
            'isCorrect': is_correct,
            'correctAnswer': current_quiz.answer_full if current_quiz else None
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def get_quiz_question(request):
    """問題取得API"""
    try:
        room_id = request.GET.get('roomId')
        room = Room.objects.get(roomId=room_id)
        
        quiz = QuizData1.objects.filter(
            quizId=room.quizId,
            questionId=room.currentSeq
        ).first()
        
        return JsonResponse({
            'question': QuizData1Serializer(quiz).data if quiz else None,
            'currentSeq': room.currentSeq
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)