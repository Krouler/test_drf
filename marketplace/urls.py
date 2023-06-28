from django.urls import path, include

from rest_framework.routers import SimpleRouter, DefaultRouter

from marketplace.views import ShopViewSet


routerShop = DefaultRouter()
routerShop.register(r'shop', ShopViewSet)
print(routerShop.urls)

urlpatterns = [
    path('', include(routerShop.urls)),
]

