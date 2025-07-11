from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'quizdata1', views.QuizData1ViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)), 
    path('test/error/', views.test_error, name="test_error"),
]