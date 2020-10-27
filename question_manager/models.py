from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=20)
    parent_id = models.IntegerField()
    target = models.CharField(max_length=20)
    level = models.IntegerField()
    creation_datetime = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Questions(models.Model):
    question = models.CharField(max_length=20)
    answer = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    creation_datetime = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.question

#Модель для организаций
class Organizations(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()


#Модель для подразделений
class Departments(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()
    visibility = models.BooleanField()
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)

