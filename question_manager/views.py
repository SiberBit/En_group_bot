from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from En_group_bot.settings import DEBUG
from question_manager.models import Categories
from question_manager.serializers import CategoriesSerializer


def index(request):
    categories = Categories.objects.filter(level=1)
    serializer = CategoriesSerializer(categories, many=True)
    data = {
        'DEBUG': DEBUG,
        'categories': serializer.data
    }
    return render(request, template_name='question_manager/index.html', context=data)


class CategoriesView(APIView):

    def get(self, request, id=None):
        """Получение всех категорий"""
        print(request.data)
        # try:
        #     level = request.data['level']
        # except KeyError:
        #     return Response(status=400)
        if id:
            categories = Categories.objects.filter(parent_id=id)
        else:
            categories = Categories.objects.filter(level=1)
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Создание категории"""
        print(request.data)
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
        data = request.data
        try:
            category = Categories.objects.get(id=data['id'])
        except Categories.DoesNotExist:
            return Response(status=404)
        data = {}
        operation = category.delete()
        if operation:
            data['success'] = 'delete successful'
        else:
            data['error'] = 'delete failed'
        return Response(data=data)
