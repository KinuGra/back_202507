from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/error/', views.test_error, name="test_error"),
]