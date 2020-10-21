from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tg_bot/', include('tg_bot.urls')),
    path('question_manager/', include('question_manager.urls'), name='question_manager'),
    path('', RedirectView.as_view(url='question_manager/'), name='home'),
]
