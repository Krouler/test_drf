from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auth_user.views import UpdateUserViewSet, RetrieveOrCreateProfileViewSet, RegistrationApiView, \
    UpdateUserPasswordViewSet, CartGenericViewSet

routerCart = DefaultRouter()
routerCart.register(r'cart', CartGenericViewSet, basename='cart')


urlpatterns = [
    path('registration/', RegistrationApiView.as_view(), name='create-user'),
    path('me/', RetrieveOrCreateProfileViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='my-profile'),
    path('me/update/', UpdateUserViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
         name='update-profile'),
    path('me/password/', UpdateUserPasswordViewSet.as_view({'post': 'create'}),
         name='update-password'),
    path('me/', include(routerCart.urls)),
    path('me/cart/all/', CartGenericViewSet.as_view({'delete': 'destroy_all'}), name='cart-destroy_all')
]
