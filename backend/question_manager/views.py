from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render

from En_group_bot.settings import DEBUG
from question_manager.models import Category, Question, Organization, Department
from question_manager.permissions import IsAuthorizedOrganization
from question_manager.serializers import CategoriesSerializer, QuestionsSerializer, OrganizationSerializer, \
    DepartmentSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser


def index(request):
    categories = Category.objects.filter(level=1)
    serializer = CategoriesSerializer(categories, many=True)
    data = {
        'DEBUG': DEBUG,
        'categories': serializer.data
    }
    return render(request, template_name='question_manager/index.html', context=data)


class OrganizationViewSet(viewsets.ModelViewSet):
    """Организации"""
    permission_classes = [IsAdminUser]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class UserOrganizationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Организации пользователя"""
        organizations = request.user.profile.organization.all()
        serializer = OrganizationSerializer(organizations, many=True)

        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    """Подразделения"""
    permission_classes = [IsAdminUser]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class OrganizationsDepartmentsView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorizedOrganization]

    def get(self, request, organization: str):
        """Подразделения организации"""

        departments = Department.objects.filter(organization__slug=organization)
        serializer = DepartmentSerializer(departments, many=True)

        return Response(serializer.data)


class CategoryView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorizedOrganization]

    def get(self, request, organization, department, pk):
        """Получение информации о категории по id"""
        try:
            categories = Category.objects.get(id=pk, department__slug=department,
                                              department__organization__slug=organization)
        except Category.DoesNotExist:
            return Response(status=404)

        serializer = CategoriesSerializer(categories)

        return Response(serializer.data)

    def post(self, request, **kwargs):
        """Создание категории"""
        category = CategoriesSerializer(data=request.data)
        if category.is_valid():
            category.save()
            return Response(status=201, data=category.data)
        return Response(status=400)

    def put(self, request, organization, department, pk):
        """Изменение категории"""
        data = request.data
        try:
            category = Category.objects.get(id=pk, department__slug=department,
                                            department__organization__slug=organization)
        except Category.DoesNotExist:
            return Response(status=404)
        serializer = CategoriesSerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400)

    def delete(self, request, organization, department):
        data = request.data
        try:
            category = Category.objects.get(id=data['id'], department__slug=department,
                                            department__organization__slug=organization)
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
    permission_classes = [IsAuthenticated, IsAuthorizedOrganization]

    def get(self, request, organization, department, pk=None):
        """Получение всех категорий"""
        if pk:
            categories = Category.objects.filter(parent_id=pk, department__slug=department,
                                                 department__organization__slug=organization)
        else:
            categories = Category.objects.filter(level=1, department__slug=department,
                                                 department__organization__slug=organization)
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)


class QuestionView(APIView):

    def get(self, request, organization, department, pk):
        """Получение информации о вопросе по id"""
        try:
            question = Question.objects.get(id=pk, category__department__slug=department,
                                            category__department__organization__slug=organization)
        except Question.DoesNotExist:
            return Response(status=404)
        serializer = QuestionsSerializer(question)

        return Response(serializer.data)

    def post(self, request, **kwargs):
        """Создание категории"""
        questions = QuestionsSerializer(data=request.data)
        if questions.is_valid():
            questions.save()
            return Response(status=201, data=questions.data)
        return Response(status=400)

    def put(self, request, organization, department):
        """Изменение категории"""
        data = request.data
        try:
            questions = Question.objects.get(id=data['id'], category__department__slug=department,
                                             category__department__organization__slug=organization)
        except Question.DoesNotExist:
            return Response(status=404)
        serializer = QuestionsSerializer(questions, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400)

    def delete(self, request, organization, department):
        data = request.data
        try:
            questions = Question.objects.get(id=data['id'], category__department__slug=department,
                                             category__department__organization__slug=organization)
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

    def get(self, request, category_id, organization, department):
        """Получение всех категорий"""
        questions = Question.objects.filter(category_id=category_id, category__department__slug=department,
                                            category__department__organization__slug=organization)

        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data)
