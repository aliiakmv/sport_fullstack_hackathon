from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH']:
            return request.user.is_authenticated and request.user == obj.trainer
        return request.user.is_authenticated and (request.user == obj.trainer or request.user.is_staff)

