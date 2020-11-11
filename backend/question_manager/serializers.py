from rest_framework import serializers

from question_manager.models import Category, Question, Organization, Department


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
