import uuid # UUIDを生成するためのモジュールをインポート
from django.db import models # Djangoのデータベース機能（モデル）を使うために、modelsモジュールをインポート
from django.contrib.auth.hashers import make_password # パスワードをハッシュ化するための関数をインポート

class User(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # ユーザーを一意に識別するためのUUIDフィールド
    username = models.CharField(max_length=150, blank=True, null=True) # ユーザー名のフィールド
    icon = models.ImageField(upload_to='user_icons/', blank=True, null=True) # ユーザーアイコンの画像フィールド
    loginId = models.CharField(max_length=150, unique=True, blank=True, null=True) 
    password = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # パスワードをハッシュ化（既にハッシュ化されているなら無視）
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username or 'Guest'} ({self.uuid})"