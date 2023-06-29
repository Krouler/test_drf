from django.urls import path, include

from rest_framework.routers import SimpleRouter, DefaultRouter

from marketplace.routers import ShopRouter, ConfDataRouter
from marketplace.views import ShopViewSet, ConfDataUpdateAPIView

routerShop = DefaultRouter()
routerShop.register(r'shop', ShopViewSet)

urlpatterns = [
    path('', include(routerShop.urls)),
    path('shop/<slug_name>/confdata/', ConfDataUpdateAPIView.as_view({'put': 'update', 'patch': 'partial_update'}), name='confdata-detail'),
]

