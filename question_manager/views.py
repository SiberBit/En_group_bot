from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from question_manager.models import Categories
from question_manager.serializers import CategoriesSerializer


def index(request):
    return HttpResponse('Hello from manager!')


class CategoriesView(APIView):

    def get(self, request):
        """Получение всех категорий"""
        level = request.data['level']
        categories = Categories.objects.filter(level=level)
        serializer = CategoriesSerializer(categories, many=True)
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
        pass

    def delete(self, request):
        """Удаление категории"""
        pass
