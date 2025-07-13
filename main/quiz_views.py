from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
import random
import requests
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
        
        # 最初の問題を取得してPusherで配信
        quiz = QuizData1.objects.filter(quizId=room.quizId, questionId=0).first()
        
        if quiz:
            trigger_question_display(room_id, {
                'question': QuizData1Serializer(quiz).data,
                'questionIndex': 0
            })
        
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
        print('Submit answer request data:', data)
        room_id = data.get('roomId')
        user_uuid = data.get('userUuid')
        answer = data.get('answer')
        print(f'Parsed data - roomId: {room_id}, userUuid: {user_uuid}, answer: {answer}')
        
        try:
            room = Room.objects.get(roomId=room_id)
            print(f'Found room: {room.id}, status: {room.status}, currentSeq: {room.currentSeq}')
        except Room.DoesNotExist:
            print(f'Room not found: {room_id}')
            return JsonResponse({'error': f'Room not found: {room_id}'}, status=404)
            
        try:
            user = User.objects.get(uuid=user_uuid)
            print(f'Found user by UUID: {user.uuid}')
        except User.DoesNotExist:
            print(f'User not found: {user_uuid}')
            return JsonResponse({'error': f'User not found: {user_uuid}'}, status=404)
        
        # 現在の問題を取得
        current_quiz = QuizData1.objects.filter(
            quizId=room.quizId,
            questionId=room.currentSeq
        ).first()
        
        is_correct = current_quiz and answer == current_quiz.answer_full
        
        # 回答を記録
        print(f'Creating answer record - roomPK_id: {room.id}, uuid: {str(user.uuid)}, roomId: {room.id}')
        Answer.objects.create(
            roomPK_id=room.id,
            uuid=str(user.uuid),
            roomId=room.id,
            currentSeq=room.currentSeq,
            quizId=room.quizId,
            questionId=current_quiz.questionId if current_quiz else 0,
            isCorrect=is_correct
        )
        print('Answer record created successfully')
        
        # Pusherで結果を配信
        trigger_answer_result(room.roomId, {
            'userId': str(user.uuid),
            'isCorrect': is_correct,
            'correctAnswer': current_quiz.answer_full if current_quiz else None
        })
        
        # 正解の場合、スコアを加算して次の問題に進む
        if is_correct:
            # スコア加算
            participant, created = RoomParticipants.objects.get_or_create(
                roomId=room.id,
                uuid=str(user.uuid),
                defaults={'currentScore': 0}
            )
            participant.currentScore += 1
            participant.save()
            print(f'Score updated for {user.uuid}: {participant.currentScore}')
            
            # スコア更新をPusherで配信
            trigger_score_update(room.roomId, {
                'userId': str(user.uuid),
                'score': participant.currentScore
            })
            
            advance_to_next_question(room)
        
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

@csrf_exempt
@require_POST
def join_room(request):
    """ルーム参加API"""
    try:
        data = json.loads(request.body)
        room_id_str = data.get('roomId')
        user_uuid = data.get('userUuid')
        
        room = Room.objects.get(roomId=room_id_str)
        user = User.objects.get(uuid=user_uuid)
        
        participant, created = RoomParticipants.objects.get_or_create(
            roomId=room.id,
            uuid=str(user.uuid),
            defaults={'currentScore': 0}
        )
        
        return JsonResponse({
            'success': True,
            'created': created
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_GET
def get_room_participants(request):
    """ルーム参加者取得API"""
    try:
        room_id_str = request.GET.get('roomId')
        print(f'Getting participants for roomId: {room_id_str}')
        
        # Room.roomIdで検索してRoom.idを取得
        room = Room.objects.get(roomId=room_id_str)
        print(f'Found room with id: {room.id}')
        
        # RoomParticipants.roomIdはRoom.idを参照
        participants = RoomParticipants.objects.filter(roomId=room.id)
        print(f'Found {participants.count()} participants')
        
        participant_data = []
        for p in participants:
            try:
                user = User.objects.get(uuid=p.uuid)
                participant_data.append({
                    'uuid': p.uuid,
                    'name': user.username or 'Anonymous',
                    'avatarUrl': user.icon or '/images/avatars/person_avatar_1.png',
                    'score': p.currentScore
                })
            except User.DoesNotExist:
                print(f'User not found for uuid: {p.uuid}')
        
        print(f'Returning {len(participant_data)} participants')
        return JsonResponse({
            'participants': participant_data
        })
    except Room.DoesNotExist:
        print(f'Room not found: {room_id_str}')
        return JsonResponse({'error': f'Room not found: {room_id_str}'}, status=404)
    except Exception as e:
        print(f'Error getting participants: {e}')
        return JsonResponse({'error': str(e)}, status=400)

def advance_to_next_question(room):
    """次の問題に進む処理"""
    room.currentSeq += 1
    room.save()
    
    # 次の問題を取得
    next_quiz = QuizData1.objects.filter(
        quizId=room.quizId,
        questionId=room.currentSeq
    ).first()
    
    if next_quiz:
        # 次の問題をPusherで配信
        trigger_question_display(room.roomId, {
            'question': QuizData1Serializer(next_quiz).data,
            'questionIndex': room.currentSeq
        })
        return True
    else:
        # ゲーム終了
        trigger_game_end(room.roomId)
        room.status = 'finished'
        room.save()
        return False

def trigger_question_display(room_id, data):
    """問題表示イベントをPusherで送信"""
    try:
        requests.post('http://localhost:3000/api/quiz', json={
            'action': 'display_question',
            'roomId': room_id,
            'data': data
        })
    except Exception as e:
        print(f'Pusher trigger error: {e}')

def trigger_answer_result(room_id, data):
    """回答結果イベントをPusherで送信"""
    try:
        requests.post('http://localhost:3000/api/quiz', json={
            'action': 'submit_answer',
            'roomId': room_id,
            'data': data
        })
    except Exception as e:
        print(f'Pusher trigger error: {e}')

def trigger_score_update(room_id, data):
    """スコア更新イベントをPusherで送信"""
    try:
        requests.post('http://localhost:3000/api/quiz', json={
            'action': 'update_score',
            'roomId': room_id,
            'data': data
        })
    except Exception as e:
        print(f'Pusher trigger error: {e}')

def trigger_game_end(room_id):
    """ゲーム終了イベントをPusherで送信"""
    try:
        requests.post('http://localhost:3000/api/quiz', json={
            'action': 'end_game',
            'roomId': room_id,
            'data': {}
        })
    except Exception as e:
        print(f'Pusher trigger error: {e}')