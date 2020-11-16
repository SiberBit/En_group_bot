from rest_framework.permissions import BasePermission, SAFE_METHODS

from question_manager.models import ChatBot


class IsAuthorizedOrganization(BasePermission):
    """Проверяем есть ли у пользователя доступ к организации"""

    def has_permission(self, request, view):
        organization_slug = view.kwargs['organization']
        for organization in request.user.profile.organization.all():
            if organization_slug in organization.slug:
                return True
        return False


class IsChatBot(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Bot-Authorization')
        if token:
            chat_bot = ChatBot.objects.filter(token=token)
            if chat_bot:
                organization_slug = view.kwargs['organization']
                if organization_slug == chat_bot[0].department.organization.slug:
                    return True
        return False
