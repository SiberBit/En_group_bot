from django.urls import path
from question_manager import views

urlpatterns = [
    path("categories/<int:id>/", views.CategoriesView.as_view()),
    path("categories/", views.CategoriesView.as_view()),
    path("category/<int:id>/", views.CategoryView.as_view())

]
