from django.contrib import admin
from question_manager import models

admin.site.register(models.Categories)
admin.site.register(models.Questions)
