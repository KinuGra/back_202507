import uuid # UUIDを生成するためのモジュールをインポート
from django.db import models # Djangoのデータベース機能（モデル）を使うために、modelsモジュールをインポート
from django.contrib.auth.hashers import make_password  # パスワードをハッシュ化するための関数をインポート
class Item(models.Model):  # Itemという名前の新しいモデル（データベースのテーブルに対応）を作成しており、models.Modelを継承する
    # nameというフィールド（データベースの列に対応）を定義している。文字列（CharField）で最大長は100文字
    name = models.CharField(max_length=100)
    # descriptionというフィールドを定義。長いテキスト（TextField）を保存できるようにしている
    description = models.TextField()

class Room(models.Model):
    roomId = models.CharField(max_length=100, unique=True)
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='waiting')
    currentSeq = models.IntegerField()
    quizId = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    # ユーザーを一意に識別するためのUUIDフィールド
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(
        max_length=150, blank=True, null=True)  # ユーザー名のフィールド
    icon = models.ImageField(upload_to='user_icons/',
                             blank=True, null=True)  # ユーザーアイコンの画像フィールド
    loginId = models.CharField(
        max_length=150, unique=True, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # パスワードをハッシュ化（既にハッシュ化されているなら無視）
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username or 'Guest'} ({self.uuid})"


class QuizData1(models.Model):
    questionId = models.IntegerField(unique=True)
    quizId = models.IntegerField()
    question = models.TextField(max_length=255)
    answer_letters = models.JSONField(blank=True, null=True)
    answer_full = models.TextField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Quiz {self.questionId}: {self.question[:20]}..."
