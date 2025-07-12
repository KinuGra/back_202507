from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.decorators import action  # DRFのアクションデコレータをインポート。特定のHTTPメソッドに対応するカスタムアクションを定義するために使用
from rest_framework.response import Response  # DRFのレスポンスをインポート。
from rest_framework import viewsets # DRFからviewsetsをインポート。ウェブページの表示やデータ処理などの一連の操作をひとまとめにしたクラス（=ビューセット）
from .models import Item, Room, Ranking, QuizData1, QuizData2, QuizData3, RoomParticipants, Answer, Summary, User # 同じディレクトリにあるmodels.pyファイルからItemモデルとRoomモデルをインポート
from .serializers import ItemSerializer, RoomParticipantsSerializer, RankingSerializer, UserSerializer, RoomSerializer, QuizData1Serializer, QuizData2Serializer, QuizData3Serializer, AnswerSerializer, SummarySerializer # 同じディレクトリにあるserializers.pyファイルからItemSerializerとRoomSerializerをインポート
from .models import Item, Room, User, QuizData1, Participantion # 同じディレクトリにあるmodels.pyファイルからItemモデルをインポート

# Userモデルに対するCRUD（Create, Read, Update, Delete）操作を処理するUserViewSetクラスを定義
# viewsets.ModelViewSetを継承している
class UserViewSet(viewsets.ModelViewSet):
    # Userモデルから全てのオブジェクトを取得する
    queryset = User.objects.all()
    # このビューセットで使用するシリアライザクラスをUserSerializerに指定している。
    # これにより、クライアントとのデータ交換時にUserオブジェクトのシリアライズ（データ形式の変換）とデシリアライズ（元のデータ形式への復元）が行われる。
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], url_path='by-room')
    def by_room(self, request):
        room_id = request.query_params.get('roomId')
        if not room_id:
            return Response({'error': 'roomId is required'}, status=400)
        
        participations = RoomParticipants.objects.filter(roomId=room_id)
        users = [p.uuid for p in participations]

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class QuizData1ViewSet(viewsets.ModelViewSet):
    queryset = QuizData1.objects.all()
    serializer_class = QuizData1Serializer

class QuizData2ViewSet(viewsets.ModelViewSet):
    queryset = QuizData2.objects.all()
    serializer_class = QuizData2Serializer

class QuizData3ViewSet(viewsets.ModelViewSet):
    queryset = QuizData3.objects.all()
    serializer_class = QuizData3Serializer

class RoomParticipantsViewSet(viewsets.ModelViewSet):
    queryset = RoomParticipants.objects.all()
    serializer_class = RoomParticipantsSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer

class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer

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