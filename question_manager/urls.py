from django.urls import path
from question_manager import views

urlpatterns = [
    path("сategories/", views.CategoriesView.as_view()),
    path('', views.index),

]
