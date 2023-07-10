from django.contrib.auth.models import User
from rest_framework import mixins, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from auth_user.models import Profile
from auth_user.permissions import NotAuthed
from auth_user.serializer import UpdateUserSerializer, SelfProfileSerializer, CreateUserSerializer, \
    UpdatePasswordSerializer


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

