from rest_framework import serializers # Django REST Frameworkのserializersモジュールをインポート
from .models import Item, Room, User, Room, QuizData1 # 同じディレクトリにあるmodels.pyファイルからItemモデルとRoomモデルをインポート

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