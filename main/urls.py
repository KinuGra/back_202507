from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, quiz_views, debug_views

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
    path('api/quiz/start/', quiz_views.start_quiz_game, name='start_quiz_game'),
    path('api/quiz/submit/', quiz_views.submit_answer, name='submit_answer'),
    path('api/quiz/question/', quiz_views.get_quiz_question, name='get_quiz_question'),
    path('api/quiz/participants/', quiz_views.get_room_participants, name='get_room_participants'),
    path('api/quiz/join/', quiz_views.join_room, name='join_room'),
    path('api/debug/database/', debug_views.database_debug, name='database_debug'),
    path('test/error/', views.test_error, name="test_error"),
]