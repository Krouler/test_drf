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


# class IsMaintainerOrIsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_staff and request.user.is_available:
#             return True
#         if request.user.is_authenticated and request.user.is_available:
#             return bool(len(request.user.shops_maintainer.all()) > 0)
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         return bool(request.user == obj.main_employee or request.user.is_staff)


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


class IsMaintainerOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_active:
                if request.user.is_staff:
                    return True
                count_of_shops_maintained_by = len(request.user.shops_maintainer.all())
                return count_of_shops_maintained_by > 0
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.user == obj.main_employee


class IsMaintainerOrIsAdminForRetrieveProfileFromCode(IsMaintainerOrIsAdmin):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request=request, view=view)


class IsEmployeeOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or request.user in obj.select_related('shop').shop.employee.all())


class IsAuthenticatedOrCommentOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return bool(obj.user == request.user or request.method in SAFE_METHODS)
        return bool(request.method in SAFE_METHODS)
