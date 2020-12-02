from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render

from En_group_bot.settings import DEBUG
from question_manager.models import Category, Question, Organization, Department, ChatBot
from question_manager.permissions import IsAuthorizedOrganization, IsChatBot
from question_manager.serializers import CategoriesSerializer, QuestionsSerializer, OrganizationSerializer, \
    DepartmentSerializer, ChatBotReadSerializer, ChatBotWriteSerializer

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
        departments_serializer = DepartmentSerializer(departments, many=True)
        departments = departments_serializer.data

        chat_bots = ChatBot.objects.filter(organization__slug=organization)
        chat_bots_serializer = ChatBotReadSerializer(chat_bots, many=True)
        chat_bots = chat_bots_serializer.data

        for department in departments:
            if not dict(department).get('chat_bot'):
                department['chat_bot'] = []
            for chat_bot in chat_bots:
                if chat_bot['department']['id'] == department['id']:
                    department['chat_bot'].append(chat_bot)

        return Response(departments)


class CategoryView(APIView):
    permission_classes = [IsChatBot | (IsAuthenticated & IsAuthorizedOrganization)]

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
        return Response(status=400, data=category.errors)

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
        return Response(status=400, data=serializer.errors)

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
    permission_classes = [IsChatBot | (IsAuthenticated & IsAuthorizedOrganization)]

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
    permission_classes = [IsChatBot | (IsAuthenticated & IsAuthorizedOrganization)]

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
        """Создание вопроса"""
        questions = QuestionsSerializer(data=request.data)
        if questions.is_valid():
            questions.save()
            return Response(status=201, data=questions.data)
        return Response(status=400, data=questions.errors)

    def put(self, request, organization, department, pk):
        """Изменение вопроса"""
        data = request.data
        try:
            questions = Question.objects.get(id=pk, category__department__slug=department,
                                             category__department__organization__slug=organization)
        except Question.DoesNotExist:
            return Response(status=404)
        serializer = QuestionsSerializer(questions, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400, data=serializer.errors)

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
    permission_classes = [IsChatBot | (IsAuthenticated & IsAuthorizedOrganization)]

    def get(self, request, organization, department, category_id):
        """Получение всех вопросов"""
        questions = Question.objects.filter(category_id=category_id, category__department__slug=department,
                                            category__department__organization__slug=organization)
        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data)


class ChatBotView(APIView):
    permission_classes = [IsAuthenticated & IsAuthorizedOrganization]

    def get(self, request, organization=None, pk=None):
        """Получение информации о чат боте по id"""
        try:
            chat_bot = ChatBot.objects.get(id=pk, organization__slug=organization)
        except ChatBot.DoesNotExist:
            return Response(status=404)
        serializer = ChatBotReadSerializer(chat_bot)

        return Response(serializer.data)

    def post(self, request, **kwargs):
        """Добавление чат бота"""
        chat_bot = ChatBotWriteSerializer(data=request.data)
        if chat_bot.is_valid():
            chat_bot.save()
            return Response(status=201, data=chat_bot.data)
        return Response(status=400, data=chat_bot.errors)

    def put(self, request, organization=None, pk=None):
        """Изменение чат бота"""
        data = request.data
        try:
            chat_bot = ChatBot.objects.get(id=pk, organization__slug=organization)
        except ChatBot.DoesNotExist:
            return Response(status=404)
        serializer = ChatBotWriteSerializer(chat_bot, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400, data=serializer.errors)

    def delete(self, request, organization=None):
        data = request.data
        try:
            chat_bot = ChatBot.objects.get(id=data['id'], organization__slug=organization)
        except ChatBot.DoesNotExist:
            return Response(status=404)
        data = {}
        operation = chat_bot.delete()
        if operation:
            data['success'] = 'delete successful'
        else:
            data['error'] = 'delete failed'
        return Response(data=data)


class ChatBotsView(APIView):
    permission_classes = [IsAuthenticated & IsAuthorizedOrganization]

    def get(self, request, organization=None):
        """Получение всех чат ботов"""
        chat_bot = ChatBot.objects.filter(organization__slug=organization)
        serializer = ChatBotReadSerializer(chat_bot, many=True)
        return Response(serializer.data)
