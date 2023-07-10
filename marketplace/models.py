from django.contrib.auth.models import User
from django.db import models

from marketplace.models_base import ShopBaseModel, ProductBaseModel, StashBaseModel, CommentBaseModel


def get_image_path_for_stash(instance, filename):
    return 'shops_{0}/stash/{1}/{2}'.format(instance.shop.id, instance.article, filename)


def get_image_path_for_shop(instance, filename):
    return 'shops_{0}/image/{1}'.format(instance.shop.id, filename)


class Shop(ShopBaseModel):

    def __str__(self):
        return self.name_short


class ConfidentialInfoShop(models.Model):
    shop = models.OneToOneField(Shop, related_name='confdata', on_delete=models.CASCADE)
    employee = models.ManyToManyField(User, related_name='shops', verbose_name='Сотрудник', blank=False)
    main_employee = models.ForeignKey(User, related_name='shops_maintainer', on_delete=models.PROTECT)

    def __str__(self):
        return f'conf {self.shop.name}'


class Product(ProductBaseModel):
    shop = models.ManyToManyField(Shop, through='Stash')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Stash(StashBaseModel):
    product = models.ForeignKey(Product, related_name='shops', verbose_name='Продукт', on_delete=models.PROTECT)
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE, verbose_name='Магазин')
    count = models.PositiveIntegerField(default=0, blank=True, verbose_name='Количество')
    is_delivery_available = models.BooleanField(default=False, blank=True, verbose_name='Доступность доставки')

    def __str__(self):
        return f'{self.article}.{self.shop.name_short if self.shop.name_short is not None else self.shop.name}: {self.product.name}'

    class Meta:
        verbose_name = 'Продукт в магазине'
        verbose_name_plural = 'Продукты в магазине'


class CommentShopProduct(CommentBaseModel):

    stash = models.ForeignKey(Stash, related_name='comments', on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, related_name='comments_to_product', null=True, verbose_name='Комментатор',
                             on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.profile.last_name} {self.user.profile.first_name}: {self.caption}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
