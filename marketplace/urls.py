from django.urls import path, include

from rest_framework.routers import DefaultRouter

from marketplace.views import ShopViewSet, ConfDataUpdateAPIView, ProductViewSet

routerShop = DefaultRouter()
routerShop.register(r'shop', ShopViewSet)
routerProduct = DefaultRouter()
routerProduct.register(r'product', ProductViewSet, basename='product')
routerShop.registry.extend(routerProduct.registry)

urlpatterns = [
    path('', include(routerShop.urls)),
    path('shop/<slug_name>/confdata/', ConfDataUpdateAPIView.as_view({'put': 'update', 'patch': 'partial_update'}), name='confdata-detail'),

]

