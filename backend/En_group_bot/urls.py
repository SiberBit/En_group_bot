from django.contrib import admin

from django.urls import path, include
from django.views.generic import RedirectView

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

from En_group_bot.token import CustomTokenObtainPairView
from question_manager.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/', include('question_manager.urls')),

    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),

    path('user/', include('profiles.urls')),

    path('', index, name='home')
]



