from django.contrib import admin
from question_manager import models

admin.site.register(models.Category)
admin.site.register(models.Question)
admin.site.register(models.Organization)
admin.site.register(models.Department)
admin.site.register(models.ChatBot)
