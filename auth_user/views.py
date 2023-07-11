from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import mixins, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from auth_user.models import Profile, Cart
from auth_user.permissions import NotAuthed
from auth_user.serializer import UpdateUserSerializer, SelfProfileSerializer, CreateUserSerializer, \
    UpdatePasswordSerializer, CartSerializer


class UpdateUserViewSet(mixins.UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        if hasattr(request.user, 'profile'):
            return super().update(request, *args, **kwargs)
        return Response(
            {'detail': 'you need to create profile by /POST/ method to /user/me/ url before you will enter to profile',
             'url': reverse('my-profile')})


class RetrieveOrCreateProfileViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SelfProfileSerializer

    def get_object(self):
        return self.request.user.profile

    def retrieve(self, request, *args, **kwargs):
        if hasattr(request.user, 'profile'):
            return super().retrieve(request, *args, **kwargs)
        return Response(
            {'detail': 'you need to create profile by /POST/ method to /user/me/ url before you will enter to profile',
                'url': reverse('my-profile')})

    def create(self, request, *args, **kwargs):
        if hasattr(request.user, 'profile'):
            return Response(
                {'detail': 'You already created profile. You need use /PUT/ or /PATCH/ method to update profile on /user/me/update/ url.',
                 'url': reverse('update-profile')}
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class RegistrationApiView(CreateAPIView):
    model = User
    permission_classes = (NotAuthed,)
    serializer_class = CreateUserSerializer


class UpdateUserPasswordViewSet(mixins.CreateModelMixin, GenericViewSet):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        obj = self.get_object()
        if serializer.is_valid(raise_exception=True):
            if not obj.check_password(serializer.validated_data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            obj.set_password(serializer.validated_data.get("new_password"))
            obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartGenericViewSet(mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    queryset = None
    cost_for_buy_operation = None
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        if self.queryset is not None:
            return self.queryset
        if hasattr(self.request.user.profile, 'cart'):
            return self.request.user.profile.cart.items.select_related('product').all()
        cart_obj = Cart.objects.create(profile=self.request.user.profile)
        self.queryset = cart_obj.items.all()
        return self.queryset

    def destroy_all(self, request, *args, **kwargs):
        qs = request.user.profile.cart.items.all()
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def sum_costs_of_all_items_in_cart(self):
        qs = self.queryset if self.queryset is not None else self.get_queryset()
        sum_result = 0
        for item in qs:
            sum_result += item.product.cost * item.count
        self.cost_for_buy_operation = sum_result
        return sum_result

    def buy_operation(self):
        profile = self.request.user.profile
        costs = self.cost_for_buy_operation if self.cost_for_buy_operation is not None else self.sum_costs_of_all_items_in_cart()
        if profile.balance < costs:
            raise Exception(f'Не достаточно денег на балансе для совершения покупки! Итого: {costs}, а ваш баланс - {profile.balance}')
        qs = self.queryset if self.queryset is not None else self.get_queryset()
        for item in qs:
            product = item.product
            if item.count > product.count:
                raise Exception(f'Не достаточно товара на складе! "{item.product.name}" было запрошено {item.count} штук, но на складе есть {item.product.count}!')
            product.count -= item.count
            product.save()
        profile.balance -= costs
        profile.save()
        qs.all().delete()

    def perform_create(self, serializer):
        if serializer.validated_data.get('operation') == 'buy':
            try:
                with transaction.atomic():
                    self.buy_operation()
            except Exception as e:
                return Response({'error': str(e)})
        else:
            serializer.save()

