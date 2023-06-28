from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission, SAFE_METHODS

from marketplace.models import Shop
from marketplace.serializers import ShopSerializer, ShopSerializerForCustomer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    permission_classes = [IsAdminUser|ReadOnly]
    lookup_field = 'slug_name'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            self.serializer_class = ShopSerializer
        else:
            self.serializer_class = ShopSerializerForCustomer
        return self.serializer_class
