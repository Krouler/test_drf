from rest_framework.permissions import BasePermission, SAFE_METHODS, BasePermissionMetaclass


class IsMaintainerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.confdata.main_employee == request.user


class IsMaintainer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff and request.user.is_available)

    def has_object_permission(self, request, view, obj):
        print(f'user: {request.user}; main_employee: {obj.main_employee}; user.is_stuff: {request.user.is_staff}. HAS_PERMISSION: {bool(request.user == obj.main_employee or request.user.is_staff)}')
        return bool(request.user == obj.main_employee or request.user.is_staff)
