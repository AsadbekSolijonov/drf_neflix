from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    SAFETY_METHODS = ('GET', 'OPTIONS', "HEAD")

    # model (request) level permission
    def has_permission(self, request, view):
        if request.user.is_staff and request.method in IsSuperUser.SAFETY_METHODS:
            return True

        return request.user.is_superuser


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser and request.method == 'GET':
            return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return request.method == 'GET' or request.user == obj
        return request.user == obj
