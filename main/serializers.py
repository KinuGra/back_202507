from rest_framework import serializers # Django REST Frameworkのserializersモジュールをインポート
from .models import User # 同じディレクトリにあるmodels.pyファイルからUserモデルをインポート

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
