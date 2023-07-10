from django.urls import path, include

from rest_framework.routers import DefaultRouter

from marketplace.views import ShopViewSet, ConfDataAPIView, ProductViewSet, RetrieveUserInfoFromCode

routerShop = DefaultRouter()
routerShop.register(r'shop', ShopViewSet)
routerProduct = DefaultRouter()
routerProduct.register(r'product', ProductViewSet, basename='product')
routerShop.registry.extend(routerProduct.registry)

urlpatterns = [
    path('', include(routerShop.urls)),
    path('shop/<slug_name>/confdata/', ConfDataAPIView.as_view({'put': 'update', 'patch': 'partial_update', 'get': 'retrieve'}), name='confdata-detail'),
    path('check_user/', RetrieveUserInfoFromCode.as_view({'post': 'create'}), name='shop-invite_employee'),
]

