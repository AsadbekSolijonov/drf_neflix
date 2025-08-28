from rest_framework.permissions import BasePermission, SAFE_METHODS, AllowAny


class IsSuperUser(BasePermission):

    # model (request) level permission
    def has_permission(self, request, view):
        if request.user.is_staff and request.method in SAFE_METHODS:
            return True

        return request.user.is_superuser


# class IsOwner(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#
#         if request.method == 'POST':
#             return bool(
#                 request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff))
#
#         if request.method == 'PATCH':
#             return bool(request.user)
#
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#
#         if user.is_superuser or user.is_staff:
#             return request.method in SAFE_METHODS
#
#         return user == obj

# Barcha view ochiq. (GET, POST, PUT, DELETE, PATCH)
class AllowAny(BasePermission):
    # View-level-permission ✅
    # Object-level-permission ❌
    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):
    # View-level-permission ✅
    # Object-level-permission ❌
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAuthenticatedOrReadOnly(BasePermission):
    # View-level-permission ✅
    # Object-level-permission ❌
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


class IsStoreAdmin(BasePermission):
    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        pass


class IsOwnerOrSuperuser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj or request.user.is_superuser)


class IsPremium(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and request.user.is_authenticated and request.user.groups.filter(name='premium_user').exists())


class TimeCheckerPermission(BasePermission):
    def has_permission(self, request, view):
        import datetime
        now = datetime.datetime.now().time()
        start = datetime.time(9, 0)
        end = datetime.time(18, 0)
        print(start, now, end)
        return start <= now <= end
