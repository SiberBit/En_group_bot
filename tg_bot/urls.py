from django.urls import path
from En_group_bot.settings import TG_TOKEN
from tg_bot import views

urlpatterns = [
    path(f'{TG_TOKEN}/', views.webhook)
]
