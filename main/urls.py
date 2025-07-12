from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'quizdata1', views.QuizData1ViewSet)
router.register(r'quizdata2', views.QuizData2ViewSet)
router.register(r'quizdata3', views.QuizData3ViewSet)
router.register(r'roomparticipants', views.RoomParticipantsViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'summaries', views.SummaryViewSet)
router.register(r'rankings', views.RankingViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/room-exists/', views.room_exists_api, name='room_exists'),
    path('test/error/', views.test_error, name="test_error"),
]