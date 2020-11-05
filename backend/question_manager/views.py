from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render

from En_group_bot.settings import DEBUG
from question_manager.models import Category, Question
from question_manager.serializers import CategoriesSerializer, QuestionsSerializer

from rest_framework.permissions import IsAuthenticated

def index(request):
    categories = Category.objects.filter(level=1)
    serializer = CategoriesSerializer(categories, many=True)
    data = {
        'DEBUG': DEBUG,
        'categories': serializer.data
    }
    return render(request, template_name='question_manager/index.html', context=data)


class CategoryView(APIView):

    def get(self, request, id):
        """Получение информации о категории по id"""
        categories = Category.objects.get(id=id)
        serializer = CategoriesSerializer(categories)

        return Response(serializer.data)

    def post(self, request):
        """Создание категории"""
        category = CategoriesSerializer(data=request.data)
        if category.is_valid():
            category.save()
            return Response(status=201, data=category.data)
        return Response(status=400)

    def put(self, request):
        """Изменение категории"""
        data = request.data
        try:
            category = Category.objects.get(id=data['id'])
        except Category.DoesNotExist:
            return Response(status=404)
        serializer = CategoriesSerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400)

    def delete(self, request):
        data = request.data
        try:
            category = Category.objects.get(id=data['id'])
        except Category.DoesNotExist:
            return Response(status=404)
        data = {}
        operation = category.delete()
        if operation:
            data['success'] = 'delete successful'
        else:
            data['error'] = 'delete failed'
        return Response(data=data)


class CategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        """Получение всех категорий"""
        if id:
            categories = Category.objects.filter(parent_id=id)
        else:
            categories = Category.objects.filter(level=1)
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)


class QuestionView(APIView):

    def get(self, request, id):
        """Получение информации о вопросе по id"""
        question = Question.objects.get(id=id)
        serializer = QuestionsSerializer(question)

        return Response(serializer.data)

    def post(self, request):
        """Создание категории"""
        questions = QuestionsSerializer(data=request.data)
        if questions.is_valid():
            questions.save()
            return Response(status=201, data=questions.data)
        return Response(status=400)

    def put(self, request):
        """Изменение категории"""
        data = request.data
        try:
            questions = Question.objects.get(id=data['id'])
        except Question.DoesNotExist:
            return Response(status=404)
        serializer = QuestionsSerializer(questions, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400)

    def delete(self, request):
        data = request.data
        try:
            questions = Question.objects.get(id=data['id'])
        except Question.DoesNotExist:
            return Response(status=404)
        data = {}
        operation = questions.delete()
        if operation:
            data['success'] = 'delete successful'
        else:
            data['error'] = 'delete failed'
        return Response(data=data)


class QuestionsView(APIView):

    def get(self, request, category_id):
        """Получение всех категорий"""

        questions = Question.objects.filter(category_id=category_id)

        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data)
