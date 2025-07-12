from django.contrib import admin
from django.utils.html import format_html
from .models import Room, User, QuizData1, QuizData2, QuizData3, RoomParticipants, Answer, Summary, Ranking

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'roomId', 'status', 'currentSeq', 'quizId', 'created_at']
    search_fields = ['roomId', 'status', 'quizId']

class UserAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'username', 'icon_tag', 'loginId', 'created_at']
    search_fields = ['username', 'loginId', 'uuid']

    def icon_tag(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;" />', obj.icon.url)
        return "-"
    icon_tag.short_description = 'Icon'

class QuizData1Admin(admin.ModelAdmin):
    list_display = ['questionId', 'quizId', 'question', 'answer_letters', 'answer_full', 'category']
    search_fields = ['question', 'answer_letters', 'category']

class QuizData2Admin(admin.ModelAdmin):
    list_display = ['questionId', 'quizId', 'question', 'answer_letters', 'answer_full', 'category']
    search_fields = ['question', 'answer_letters', 'category']

class QuizData3Admin(admin.ModelAdmin):
    list_display = ['questionId', 'quizId', 'question', 'answer_letters', 'answer_full', 'category']
    search_fields = ['question', 'answer_letters', 'category']

class RoomParticipantsAdmin(admin.ModelAdmin):
    list_display = ['roomId', 'uuid', 'currentScore', 'joined_at']
    search_fields = ['roomId_roomId', 'uuid_username']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['roomPK_id', 'uuid', 'roomId', 'currentSeq', 'answerTime', 'quizId', 'questionId', 'isCorrect']
    search_fields = ['roomPK_id__roomId', 'uuid__username', 'roomId__roomId', 'quizId', 'questionId']

class SummaryAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'totalQuestions', 'correctAnswers', 'finalScore', 'finalRank', 'created_at']
    search_fields = ['uuid__username', 'finalRank']

class RankingAdmin(admin.ModelAdmin):
    list_display = ['username', 'finalScore']
    search_fields = ['username']


admin.site.register(Room, RoomAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(QuizData1, QuizData1Admin)
admin.site.register(QuizData2, QuizData2Admin)
admin.site.register(QuizData3, QuizData3Admin)
admin.site.register(RoomParticipants, RoomParticipantsAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(Ranking, RankingAdmin)

