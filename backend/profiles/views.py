from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.serializers import UserSerializer, ProfileSerializer


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Информация о пользователе"""

        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data)
