from rest_framework import serializers

from question_manager.models import Category, Question


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
