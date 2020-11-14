from rest_framework import serializers
from django.contrib.auth.models import User

from profiles.models import Profile

from question_manager.serializers import OrganizationSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """Профиль"""
    organization = OrganizationSerializer(many=True)

    class Meta:
        model = Profile

        fields = ('organization',)


class UserSerializer(serializers.ModelSerializer):
    """Пользователь"""
    profile = ProfileSerializer()

    class Meta:
        model = User

        fields = ('id', 'username', 'profile')
