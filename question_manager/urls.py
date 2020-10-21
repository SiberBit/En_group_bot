from django.urls import path
from question_manager import views

urlpatterns = [
    path('', views.index),

    path('categories/get-all', views.get_all_categories),
    path('categories/create', views.create_category),
    path('categories/remove', views.remove_category),
    path('categories/change', views.change_category),

    path('questions/get-all', views.get_all_questions),
    path('questions/create', views.create_question),
    path('questions/remove', views.remove_question),
    path('questions/change', views.change_question),

]
