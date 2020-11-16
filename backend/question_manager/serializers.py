from rest_framework import serializers

from question_manager.models import Category, Question, Organization, Department, ChatBot


class OrganizationSerializer(serializers.ModelSerializer):
    """Организации"""

    class Meta:
        model = Organization
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    """Подразделения"""

    class Meta:
        model = Department
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    """Категории"""

    class Meta:
        model = Category
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    """Вопросы"""

    class Meta:
        model = Question
        fields = '__all__'


class ChatBotReadSerializer(serializers.ModelSerializer):
    """Чат боты (для чтения)"""
    department = DepartmentSerializer()

    class Meta:
        model = ChatBot
        fields = '__all__'


class ChatBotWriteSerializer(serializers.ModelSerializer):
    """Чат боты (для изменения)"""
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
    )

    class Meta:
        model = ChatBot
        fields = '__all__'
