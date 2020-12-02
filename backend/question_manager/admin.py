from django.contrib import admin
from question_manager import models

admin.site.register(models.Category)
admin.site.register(models.Question)
admin.site.register(models.ChatBot)


class OrganizationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.Department, DepartmentAdmin)
