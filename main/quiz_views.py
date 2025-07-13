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
def buzz_in(request):
    """早押しAPI"""
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        user_uuid = data.get('userUuid')
        
        room = Room.objects.get(roomId=room_id)
        user = User.objects.get(uuid=user_uuid)
        
        # 早押し順位を決定
        existing_buzzes = Answer.objects.filter(
            roomId=room.id,
            currentSeq=room.currentSeq,
            questionId=room.currentSeq
        ).count()
        
        # 早押し記録を作成
        buzz_record = Answer.objects.create(
            roomPK_id=room.id,
            uuid=str(user.uuid),
            roomId=room.id,
            currentSeq=room.currentSeq,
            quizId=room.quizId,
            questionId=room.currentSeq,
            isCorrect=False,  # まだ回答していない
            buzzOrder=existing_buzzes + 1
        )
        
        # 早押し結果を配信
        trigger_buzz_result(room.roomId, {
            'userId': str(user.uuid),
            'buzzOrder': buzz_record.buzzOrder,
            'hasAnswerRight': buzz_record.buzzOrder <= 3  # 上位3名に回答権
        })
        
        return JsonResponse({
            'success': True,
            'buzzOrder': buzz_record.buzzOrder,
            'hasAnswerRight': buzz_record.buzzOrder <= 3
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
        
        # 早押し記録を取得（ない場合は自動作成）
        buzz_record = Answer.objects.filter(
            roomId=room.id,
            uuid=str(user.uuid),
            currentSeq=room.currentSeq,
            questionId=room.currentSeq
        ).first()
        
        # 早押し記録がない場合は自動作成（従来の直接回答方式）
        if not buzz_record:
            buzz_record = Answer.objects.create(
                roomPK_id=room.id,
                uuid=str(user.uuid),
                roomId=room.id,
                currentSeq=room.currentSeq,
                quizId=room.quizId,
                questionId=room.currentSeq,
                isCorrect=False,
                buzzOrder=1  # 直接回答の場合は1位扱い
            )
        
        # 現在の問題を取得
        current_quiz = QuizData1.objects.filter(
            quizId=room.quizId,
            questionId=room.currentSeq
        ).first()
        
        print(f'Answer comparison: user="{answer}" vs correct="{current_quiz.answer_full if current_quiz else "None"}"')
        is_correct = current_quiz and answer == current_quiz.answer_full
        
        # 回答結果を更新
        buzz_record.isCorrect = is_correct
        buzz_record.save()
        
        # 回答結果を配信
        trigger_answer_result(room.roomId, {
            'userId': str(user.uuid),
            'isCorrect': is_correct,
            'correctAnswer': current_quiz.answer_full if current_quiz else None
        })
        
        # 正解の場合、スコア加算
        if is_correct:
            participant, created = RoomParticipants.objects.get_or_create(
                roomId=room.id,
                uuid=str(user.uuid),
                defaults={'currentScore': 0}
            )
            participant.currentScore += 1
            participant.save()
            
            trigger_score_update(room.roomId, {
                'userId': str(user.uuid),
                'score': participant.currentScore
            })
            
            # 正解者が出たら次の問題へ
            advance_to_next_question(room)
        
        return JsonResponse({
            'success': True,
            'isCorrect': is_correct,
            'correctAnswer': current_quiz.answer_full if current_quiz else None
        })
    except Exception as e:
        print(f'Submit answer error: {e}')
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
        
        # ユーザーが存在しない場合は作成
        username = data.get('username', 'Guest User')
        user, user_created = User.objects.get_or_create(
            uuid=user_uuid,
            defaults={
                'username': username,
                'icon': '/images/avatars/person_avatar_1.png',
                'loginId': None,
                'password': 'default'
            }
        )
        
        if user_created:
            print(f'Created new user: {user.uuid}')
        
        participant, created = RoomParticipants.objects.get_or_create(
            roomId=room.id,
            uuid=str(user.uuid),
            defaults={'currentScore': 0}
        )
        
        return JsonResponse({
            'success': True,
            'participant_created': created,
            'user_created': user_created
        })
    except Exception as e:
        print(f'Join room error: {e}')
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

def trigger_buzz_result(room_id, data):
    """早押し結果イベントをPusherで送信"""
    try:
        requests.post('http://localhost:3000/api/quiz', json={
            'action': 'buzz_result',
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