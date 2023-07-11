import rest_framework.filters
from django.http import Http404
from rest_framework import viewsets, mixins, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from auth_user.models import Profile
from auth_user.serializer import RetrieveUserSerializer
from marketplace.models import Shop, ConfidentialInfoShop, Product, Stash, CommentShopProduct
from marketplace.permissions import IsMaintainerOrReadOnly, IsEmployeeOrIsStaffOrReadOnly, \
    IsMaintainerOrIsAdmin, IsMaintainerOrIsAdminForRetrieveProfileFromCode, IsEmployeeOrReadOnly, \
    IsAuthenticatedOrCommentOwnerOrReadOnly
from marketplace.serializers import ShopSerializer, ShopSerializerForCustomer, ShopConfData, \
    ProductSerializerForCustomer, InviteUserSerializer, StashSerializer, CommentSerializer


class RetrieveUserInfoFromCode(mixins.CreateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = RetrieveUserSerializer
    permission_classes = (IsMaintainerOrIsAdminForRetrieveProfileFromCode,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = Profile.objects.get(invite_code=serializer.validated_data.get('invite_code'))
        except:
            return Response({'detail': 'invite code not found'}, status=status.HTTP_404_NOT_FOUND)
        response_serializer = RetrieveUserSerializer(obj)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class UpdateShopEmployeeView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = ConfidentialInfoShop.objects.all()
    serializer_class = InviteUserSerializer
    permission_classes = (IsMaintainerOrIsAdmin,)
    lookup_field = 'shop__slug_name'


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    permission_classes = (IsMaintainerOrReadOnly,)
    lookup_field = 'slug_name'

    def get_serializer_class(self):
        try:
            flag = self.request.user == self.get_object().confdata.main_employee
        except Exception:
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


class ConfDataAPIView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    obj = None
    queryset = ConfidentialInfoShop.objects.all()
    serializer_class = ShopConfData
    permission_classes = (IsMaintainerOrIsAdmin,)
    lookup_field = 'shop__slug_name'

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.check_object_permissions(request, self.get_object())

    def get_object(self):
        if self.obj is None:
            self.obj = self.queryset.get(shop__slug_name=self.kwargs.get('slug_name'))
        return self.obj


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsEmployeeOrIsStaffOrReadOnly,)
    serializer_class = ProductSerializerForCustomer

    def create_filter_kwargs(self) -> dict:
        return {'name__icontains': self.kwargs.get('name')} if self.kwargs.get('name') is not None else {}

    def get_queryset(self):
        return Product.objects.only('name').filter(**self.create_filter_kwargs())


class StashViewSet(viewsets.ModelViewSet):
    serializer_class = StashSerializer
    permission_classes = (IsEmployeeOrReadOnly,)
    queryset = Stash.objects.all()
    filterset_fields = ['cost',
                        'product__name',
                        'is_delivery_available',
                        'shop__name',
                        'shop_id',
                        'product_id',
                        'description',
                        'count']


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrCommentOwnerOrReadOnly,)
    queryset = CommentShopProduct.objects.all()
    filterset_fields = ['stash__article', 'user']
