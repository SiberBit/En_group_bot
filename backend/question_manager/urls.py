from django.urls import path
from question_manager import views

urlpatterns = [
    path("categories/<int:id>/", views.CategoriesView.as_view()),
    path("categories/", views.CategoriesView.as_view()),
    path("category/<int:id>/", views.CategoryView.as_view()),

    path("questions/<int:category_id>/", views.QuestionsView.as_view()),
    path("questions/", views.QuestionsView.as_view()),
    path("question/<int:id>/", views.QuestionView.as_view()),





]
