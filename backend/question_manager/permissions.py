from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorizedOrganization(BasePermission):
    """Проверяем есть ли у пользователя доступ к организации"""

    def has_permission(self, request, view):
        organization_slug = view.kwargs['organization']
        for organization in request.user.profile.organization.all():
            if organization_slug in organization.slug:
                return True
        return False


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff
                    or request.user.is_authenticated and request.method in SAFE_METHODS))
