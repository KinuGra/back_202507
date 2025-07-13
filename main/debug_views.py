from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Room, User, Answer, RoomParticipants, Ranking, Summary
from django.core import serializers
import json

@csrf_exempt
def database_debug(request):
    """デバッグ用：データベースの全テーブル内容を返す"""
    try:
        # 各テーブルのデータを取得
        rooms = list(Room.objects.all().values())
        users = list(User.objects.all().values())
        answers = list(Answer.objects.all().values())
        participants = list(RoomParticipants.objects.all().values())
        rankings = list(Ranking.objects.all().values())
        summaries = list(Summary.objects.all().values())
        
        return JsonResponse({
            'rooms': rooms,
            'users': users,
            'answers': answers,
            'participants': participants,
            'rankings': rankings,
            'summaries': summaries
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)