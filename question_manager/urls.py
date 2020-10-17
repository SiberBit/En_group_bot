from django.urls import path
from question_manager import views

urlpatterns = [
    path('', views.index)
]
