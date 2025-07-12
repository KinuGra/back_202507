from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework import viewsets
import pusher
import json
from .models import Item, Room, User, QuizData1
from .serializers import ItemSerializer, UserSerializer, RoomSerializer, QuizData1Serializer

# Pusher初期化
pusher_client = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)

# Userモデルに対するCRUD（Create, Read, Update, Delete）操作を処理するUserViewSetクラスを定義
# viewsets.ModelViewSetを継承している
class UserViewSet(viewsets.ModelViewSet):
    # Userモデルから全てのオブジェクトを取得する
    queryset = User.objects.all()
    # このビューセットで使用するシリアライザクラスをUserSerializerに指定している。
    # これにより、クライアントとのデータ交換時にUserオブジェクトのシリアライズ（データ形式の変換）とデシリアライズ（元のデータ形式への復元）が行われる。
    serializer_class = UserSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class QuizData1ViewSet(viewsets.ModelViewSet):
    queryset = QuizData1.objects.all()
    serializer_class = QuizData1Serializer

# ルームidが存在するかどうかを返す
@require_GET
def room_exists_api(request):
    room_id = request.GET.get('roomId')

    if not room_id:
        return JsonResponse({ 'error': 'roomId parameter is required '}, status=404)

    exists = Room.objects.filter(roomId=room_id).exists()
    return JsonResponse({ 'exists': exists })

# Create your views here.
def index(request):
    return HttpResponse("Hello, Django!")

def test_error(request):
    raise ValueError("テスト用のエラーが発生しました")

# Roomデータを取得してPusherで配信
@require_GET
def get_room_data(request):
    room_id = request.GET.get('roomId')
    if not room_id:
        return JsonResponse({'error': 'roomId required'}, status=400)
    
    try:
        room = Room.objects.get(roomId=room_id)
        room_data = RoomSerializer(room).data
        
        # Pusherでリアルタイム配信
        pusher_client.trigger(f'room-{room_id}', 'room-data', room_data)
        
        return JsonResponse(room_data)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

# Answerデータを取得してPusherで配信
@require_GET
def get_answer_data(request):
    quiz_id = request.GET.get('quizId')
    if not quiz_id:
        return JsonResponse({'error': 'quizId required'}, status=400)
    
    try:
        answers = QuizData1.objects.filter(quizId=quiz_id)
        answer_data = QuizData1Serializer(answers, many=True).data
        
        # Pusherでリアルタイム配信
        pusher_client.trigger(f'quiz-{quiz_id}', 'answer-data', answer_data)
        
        return JsonResponse({'answers': answer_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Roomステータス更新
@csrf_exempt
@require_POST
def update_room_status(request):
    data = json.loads(request.body)
    room_id = data.get('roomId')
    status = data.get('status')
    
    if not room_id or not status:
        return JsonResponse({'error': 'roomId and status required'}, status=400)
    
    try:
        room = Room.objects.get(roomId=room_id)
        room.status = status
        room.save()
        
        # 更新をPusherで通知
        pusher_client.trigger(f'room-{room_id}', 'status-updated', {
            'roomId': room_id,
            'status': status
        })
        
        return JsonResponse({'success': True})
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)