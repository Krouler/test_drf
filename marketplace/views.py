from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from marketplace.models import Shop, ConfidentialInfoShop
from marketplace.permissions import IsMaintainerOrReadOnly, IsMaintainer
from marketplace.serializers import ShopSerializer, ShopSerializerForCustomer, ShopConfData


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    permission_classes = (IsMaintainerOrReadOnly,)
    lookup_field = 'slug_name'

    def get_serializer_class(self):
        try:
            flag = self.request.user == self.get_object().confdata.main_employee
        except:
            flag = False
        if self.request.user.is_staff or flag:
            return ShopSerializer
        return ShopSerializerForCustomer

    # custom definition for perform_create
    def create_confdata(self, shop_obj):
        confdata = ConfidentialInfoShop.objects.create(shop=shop_obj, main_employee=self.request.user)
        confdata.employee.add(self.request.user)
        confdata.save()

    def perform_create(self, serializer):
        shop_new_object = serializer.save()
        self.create_confdata(shop_new_object)


class ConfDataUpdateAPIView(mixins.UpdateModelMixin, GenericViewSet):
    obj = None
    queryset = ConfidentialInfoShop.objects.all()
    serializer_class = ShopConfData
    permission_classes = (IsMaintainer,)

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.check_object_permissions(request, self.get_object())

    def get_object(self):
        if self.obj is None:
            self.obj = self.queryset.get(shop__slug_name=self.kwargs.get('slug_name'))
        return self.obj
