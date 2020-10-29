from rest_framework import serializers

from question_manager.models import Categories, Questions


class CategoriesSerializer(serializers.ModelSerializer):
    """Категории"""

    class Meta:
        model = Categories
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    """Вопросы"""

    class Meta:
        model = Questions
        fields = '__all__'
