from rest_framework import serializers # Django REST Frameworkのserializersモジュールをインポート
from .models import Answer, Item, Room, RoomParticipants, Summary, User, Room, Ranking, QuizData1, QuizData2, QuizData3 # 同じディレクトリにあるmodels.pyファイルからItemモデルとRoomモデルをインポート

'''
ItemモデルのデータをJSON形式などに変換するクラス。
簡単にシリアライズ（データ構造を連続的な形に変換）・デシリアライズ（連続的なデータを元のデータ構造に戻す）できるようにするためのItemSerializerクラスを定義しており、
serializers.ModelSerializerを継承しています
'''
class ItemSerializer(serializers.ModelSerializer):
    # ItemSerializerクラスの設定を行う内部クラスMetaを定義
    class Meta:
        # シリアライザが扱うモデルをItemに指定しています
        model = Item
        # シリアライズされるときに含めるフィールドをid、name、descriptionに限定する
        fields = ['id', 'name', 'description']

'''
RoomモデルのデータをJSON形式などに変換するクラス。
簡単にシリアライズ（データ構造を連続的な形に変換）・デシリアライズ（連続的なデータを元のデータ構造に戻す）できるようにするためのRoomSerializerクラスを定義しており、
serializers.ModelSerializerを継承しています
'''
class RoomSerializer(serializers.ModelSerializer):
    # RoomSerializerクラスの設定を行う内部クラスMetaを定義
    class Meta:
        # シリアライザが扱うモデルをRoomに指定しています
        model = Room
        # Roomモデルの全フィールドに合わせて修正
        fields = ['id', 'roomId', 'status', 'currentSeq', 'quizId', 'created_at']

'''
UserモデルのデータをJSON形式などに変換するクラス。
簡単にシリアライズ（データ構造を連続的な形に変換）・デシリアライズ（連続的なデータを元のデータ構造に戻す）できるようにするためのUserSerializerクラスを定義しており、
serializers.ModelSerializerを継承しています
'''
class UserSerializer(serializers.ModelSerializer):
    # UserSerializerクラスの設定を行う内部クラスMetaを定義
    class Meta:
        # シリアライザが扱うモデルをUserに指定しています
        model = User
        # シリアライズされるときに含めるフィールドをuuid、username、icon、loginId、password、created_atに限定する
        fields = ['uuid', 'username', 'icon', 'loginId', 'password', 'created_at']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'roomId', 'status', 'currentSeq', 'quizId', 'created_at']

class QuizData1Serializer(serializers.ModelSerializer):
    class Meta:
        model = QuizData1
        fields = ['questionId', 'quizId', 'question', 'answer_letters', 'answer_full', 'category']

class QuizData2Serializer(serializers.ModelSerializer):
    class Meta:
        model = QuizData2
        fields = ['questionId', 'quizId', 'question', 'answer_letters', 'answer_full', 'category']  

class QuizData3Serializer(serializers.ModelSerializer):
    class Meta:
        model = QuizData3
        fields = ['questionId', 'quizId', 'question', 'answer_letters', 'answer_full', 'category']  

class RoomParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomParticipants
        fields = ['roomId', 'uuid', 'currentScore', 'joined_at']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['roomPK_id', 'uuid', 'roomId', 'currentSeq', 'answerTime', 'quizId', 'questionId', 'isCorrect']

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['uuid', 'totalQuestions', 'correctAnswers', 'finalScore', 'finalRank', 'created_at']  

class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = ['username', 'finalScore']