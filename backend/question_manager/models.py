from django.db import models
from django.contrib.auth.models import User


# Модель для организаций
class Organization(models.Model):
    """Организации"""
    name = models.CharField('Название', max_length=64)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Организацию'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


# Модель для подразделений
class Department(models.Model):
    """Подразделения"""
    name = models.CharField('Название', max_length=64)
    slug = models.SlugField(unique=True)
    visibility = models.BooleanField('Для клиентов (иначе для использования внутри организации)')
    organization = models.ForeignKey(Organization, verbose_name='Организация', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории вопросов"""
    name = models.CharField('Название', max_length=64)
    parent_id = models.IntegerField('id родительской категории')
    target = models.CharField('Что будет содержать', max_length=20,
                              choices=[('categories', 'категории'), ('questions', 'вопросы')])
    level = models.IntegerField('Уровень в дереве', default=1)

    department = models.ForeignKey(Department, verbose_name='Подразделение', on_delete=models.CASCADE)

    creation_datetime = models.DateTimeField('Дата создания', auto_now=True)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Question(models.Model):
    """Вопросы"""
    question = models.CharField('Вопрос', max_length=64)
    answer = models.TextField('Ответ')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.DO_NOTHING)
    creation_datetime = models.DateTimeField('Дата создания', auto_now=True)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question


# Модель для чат-бота
class ChatBot(models.Model):
    """Чат боты"""
    name = models.CharField('Название', max_length=64)
    platform = models.CharField('Платформа', max_length=64)
    link = models.URLField('Ссылка на бота')
    organization = models.ForeignKey(Organization, verbose_name='Организация', on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department, verbose_name='Подразделение', on_delete=models.DO_NOTHING)
    description = models.TextField('Описание', max_length=100)

    class Meta:
        verbose_name = 'Чат бота'
        verbose_name_plural = 'Чат боты'

    def __str__(self):
        return self.name
