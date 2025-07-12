from django.contrib import admin
from django.utils.html import format_html
from .models import Item, Room, User, QuizData1

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)

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

admin.site.register(Item, ItemAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(QuizData1, QuizData1Admin)
