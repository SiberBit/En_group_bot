from django.urls import path, include

from profiles import views

urlpatterns = [
    path("", views.UserView.as_view()),
]
