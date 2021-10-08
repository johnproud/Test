from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = {'permission': ['You don\'t have permissions, admin only']}

    def has_permission(self, request, view):
        return request.user.is_admin
