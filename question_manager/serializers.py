from rest_framework import serializers

from question_manager.models import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    """Категории"""

    class Meta:
        model = Categories
        fields = '__all__'
