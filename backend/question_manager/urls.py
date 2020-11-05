from django.urls import path
from question_manager import views

urlpatterns = [
    path("categories/<str:organization>/<str:department>/<int:pk>/", views.CategoriesView.as_view()),
    path("categories/<str:organization>/<str:department>/", views.CategoriesView.as_view()),
    path("category/<str:organization>/<str:department>/<int:pk>/", views.CategoryView.as_view()),

    path("questions/<str:organization>/<str:department>/<int:category_id>/", views.QuestionsView.as_view()),
    path("questions/<str:organization>/<str:department>/", views.QuestionsView.as_view()),
    path("question/<str:organization>/<str:department>/<int:pk>/", views.QuestionView.as_view()),





]
