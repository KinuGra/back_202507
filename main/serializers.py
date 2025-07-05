from rest_framework import serializers # Django REST Frameworkのserializersモジュールをインポート
from .models import Item # 同じディレクトリにあるmodels.pyファイルからItemモデルをインポート

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
