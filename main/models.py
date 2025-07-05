from django.db import models # Djangoのデータベース機能（モデル）を使うために、modelsモジュールをインポート

class Item(models.Model): # Itemという名前の新しいモデル（データベースのテーブルに対応）を作成しており、models.Modelを継承する
    # nameというフィールド（データベースの列に対応）を定義している。文字列（CharField）で最大長は100文字
    name = models.CharField(max_length=100)
    # descriptionというフィールドを定義。長いテキスト（TextField）を保存できるようにしている
    description = models.TextField()