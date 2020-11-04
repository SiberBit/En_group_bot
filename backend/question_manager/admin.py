from django.contrib import admin
from question_manager import models

admin.site.register(models.Categories)
admin.site.register(models.Questions)
admin.site.register(models.Organizations)
admin.site.register(models.Departments)
admin.site.register(models.ChatBot)
