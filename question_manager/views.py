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
        try:
            level = request.data['level']
        except KeyError:
            return Response(status=400)

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
        data = request.data
        try:
            category = Categories.objects.get(id=data['id'])
        except Categories.DoesNotExist:
            return Response(status=404)

        serializer = CategoriesSerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400)

    def delete(self, request):
        """Удаление категории"""
        pass
