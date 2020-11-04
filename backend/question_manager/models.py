from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)
    parent_id = models.IntegerField()
    target = models.CharField(max_length=20, choices=[('categories', 'categories'), ('questions', 'questions')])
    level = models.IntegerField()
    creation_datetime = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=20)
    answer = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    creation_datetime = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.question


# Модель для организаций
class Organization(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()


# Модель для подразделений
class Department(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()
    visibility = models.BooleanField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


# Модель для чат-бота
class ChatBot(models.Model):
    name = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    link = models.URLField()
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=100)
