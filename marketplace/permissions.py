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
        return bool(request.user == obj.main_employee or request.user.is_staff)


class IsEmployeeOrIsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        try:
            if len(request.user.shops.all()) > 0:
                return True
        except AttributeError:
            return request.method in SAFE_METHODS
        return request.method in SAFE_METHODS




    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.method in SAFE_METHODS)
