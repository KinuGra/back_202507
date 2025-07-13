from django.db import models
from django.contrib.auth.hashers import make_password

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Room(models.Model):
    roomId = models.CharField(max_length=100, unique=True)
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    currentSeq = models.IntegerField()
    quizId = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    uuid = models.TextField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    loginId = models.CharField(max_length=150, unique=True, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class QuizData1(models.Model):
    questionId = models.IntegerField(unique=True)
    quizId = models.IntegerField()
    question = models.TextField(max_length=255)
    answer_letters = models.TextField(blank=True, null=True)
    answer_full = models.TextField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Quiz {self.questionId}: {self.question[:20]}..."

class Answer(models.Model):
    roomPK_id = models.IntegerField()
    uuid = models.TextField()
    roomId = models.IntegerField()
    currentSeq = models.IntegerField(default=0)
    answerTime = models.DateTimeField(auto_now_add=True)  # タイムスタンプに変更
    quizId = models.IntegerField()
    questionId = models.IntegerField()
    isCorrect = models.BooleanField(default=False)
    buzzOrder = models.IntegerField(default=0)  # 早押し順位

    def __str__(self):
        return f"{self.uuid} answered question {self.questionId} in room {self.roomId}"

class Summary(models.Model):
    uuid = models.TextField(unique=True)
    totalQuestions = models.IntegerField(default=0)
    correctAnswers = models.IntegerField(default=0)
    finalScore = models.IntegerField(default=0)
    finalRank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.uuid} - Score: {self.finalScore}, Rank: {self.finalRank}"

class QuizData2(models.Model):
    questionId = models.IntegerField(unique=True)
    quizId = models.IntegerField()
    question = models.TextField(max_length=255)
    answer_letters = models.TextField(blank=True, null=True)
    answer_full = models.TextField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Quiz {self.questionId}: {self.question[:20]}..."

class QuizData3(models.Model):
    questionId = models.IntegerField(unique=True)
    quizId = models.IntegerField()
    question = models.TextField(max_length=255)
    answer_letters = models.TextField(blank=True, null=True)
    answer_full = models.TextField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Quiz {self.questionId}: {self.question[:20]}..."

class Ranking(models.Model):
    username = models.CharField(max_length=150, blank=True, null=True)
    finalScore = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username or 'Anonymous'} - Score: {self.finalScore}"

class RoomParticipants(models.Model):
    roomId = models.IntegerField()
    uuid = models.TextField()
    currentScore = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('roomId', 'uuid')

    def __str__(self):
        return f"{self.uuid} in room {self.roomId}"
