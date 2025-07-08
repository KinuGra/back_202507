from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets # DRFからviewsetsをインポート。ウェブページの表示やデータ処理などの一連の操作をひとまとめにしたクラス（=ビューセット）
from .models import Item, Room # 同じディレクトリにあるmodels.pyファイルからItemモデルとRoomモデルをインポート
from .serializers import ItemSerializer, RoomSerializer # 同じディレクトリにあるserializers.pyファイルからItemSerializerとRoomSerializerをインポート
from .models import User # 同じディレクトリにあるmodels.pyファイルからUserモデルをインポート
from .serializers import UserSerializer # 同じディレクトリにあるserializers.pyファイルからUserSerializerをインポート

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

# Create your views here.
def index(request):
    return HttpResponse("Hello, Django!")

def test_error(request):
    raise ValueError("テスト用のエラーが発生しました")