from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'roomId', 'status', 'currentSeq', 'quizId', 'created_at']
    search_fields = ['roomId', 'status', 'quizId']

admin.site.register(Room, RoomAdmin)
