from rest_framework.permissions import BasePermission


class IsAuthorizedOrganization(BasePermission):
    """Проверяем есть ли у пользователя доступ к организации"""

    def has_permission(self, request, view):
        organization_slug = view.kwargs['organization']
        for organization in request.user.profile.organization.all():
            if organization_slug in organization.slug:
                return True
        return False
