from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'quizdata1', views.QuizData1ViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/room-exists/', views.room_exists_api, name='room_exists'),
    path('api/room-data/', views.get_room_data, name='get_room_data'),
    path('api/answer-data/', views.get_answer_data, name='get_answer_data'),
    path('api/update-room-status/', views.update_room_status, name='update_room_status'),
    path('test/error/', views.test_error, name="test_error"),
]