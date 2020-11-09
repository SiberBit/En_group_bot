from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorizedOrganization(BasePermission):
    """Проверяем есть ли у пользователя доступ к организации"""

    def has_permission(self, request, view):
        print(view.kwargs)
        organization_slug = view.kwargs['organization']
        for organization in request.user.profile.organization.all():
            if organization_slug in organization.slug:
                return True
        return False

