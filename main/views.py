from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets # DRFからviewsetsをインポート。ウェブページの表示やデータ処理などの一連の操作をひとまとめにしたクラス（=ビューセット）
from .models import Item # 同じディレクトリにあるmodels.pyファイルからItemモデルをインポート
from .serializers import ItemSerializer # 同じディレクトリにあるserializers.pyファイルからItemSerializerをインポート

# Itemモデルに対するCRUD（Create, Read, Update, Delete）操作を処理するItemViewSetクラスを定義
# viewsets.ModelViewSetを継承している
class ItemViewSet(viewsets.ModelViewSet):
    # Itemモデルから全てのオブジェクトを取得する
    queryset = Item.objects.all()
    # このビューセットで使用するシリアライザクラスをItemSerializerに指定している。
    # これにより、クライアントとのデータ交換時にItemオブジェクトのシリアライズ（データ形式の変換）とデシリアライズ（元のデータ形式への復元）が行われる。
    serializer_class = ItemSerializer

# Create your views here.
def index(request):
    return HttpResponse("Hello, Django!")