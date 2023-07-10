from django.urls import path

from auth_user.views import UpdateUserViewSet, RetrieveOrCreateProfileViewSet, RegistrationApiView, \
    UpdateUserPasswordViewSet

urlpatterns = [
    path('registration/', RegistrationApiView.as_view(), name='create-user'),
    path('me/', RetrieveOrCreateProfileViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='my-profile'),
    path('me/update/', UpdateUserViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
         name='update-profile'),
    path('me/password/', UpdateUserPasswordViewSet.as_view({'post': 'create'}),
         name='update-password')
]
