from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from question_manager.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tg_bot/', include('tg_bot.urls')),
    path('api/', include('question_manager.urls')),
    path('', index)
]
