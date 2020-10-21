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
