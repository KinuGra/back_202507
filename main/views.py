from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from rest_framework import viewsets # DRFからviewsetsをインポート。ウェブページの表示やデータ処理などの一連の操作をひとまとめにしたクラス（=ビューセット）
from .models import Item, Room, QuizData1 # 同じディレクトリにあるmodels.pyファイルからItemモデルとRoomモデルをインポート
from .serializers import ItemSerializer, UserSerializer, RoomSerializer, QuizData1Serializer # 同じディレクトリにあるserializers.pyファイルからItemSerializerとRoomSerializerをインポート
from .models import Item, Room, User, QuizData1 # 同じディレクトリにあるmodels.pyファイルからItemモデルをインポート

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