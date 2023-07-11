from random import randrange

from django.db import models


def get_image_path_for_stash(instance, filename):
    return 'shops_{0}/stash/{1}/{2}'.format(instance.shop.id, instance.article, filename)


def get_image_path_for_shop(instance, filename):
    return 'shops_{0}/image/{1}'.format(instance.shop.id, filename)


class StringGeneratorHelperMixin:

    @staticmethod
    def make_result(lim, prefix=''):
        result = prefix
        while len(result) < lim:
            result += str(randrange(10))
        return result

    @classmethod
    def get_qs_list(cls, only_field):
        return cls.objects.only(only_field).values_list(only_field, flat=True)


class ShopBaseModel(StringGeneratorHelperMixin, models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, unique=True, verbose_name='Полное название')
    name_short = models.CharField(max_length=20, null=False, blank=True, unique=True, default='',
                                  verbose_name='Короткое название')
    balance = models.FloatField(default=0.0, blank=True, verbose_name='Баланс магазина')
    inn = models.CharField(max_length=12, null=False, blank=False, verbose_name='ИНН')
    ceo = models.CharField(max_length=56, null=False, blank=False, verbose_name='Фамилия И.О. руководителя')
    cred_num = models.CharField(max_length=12, default='', blank=True, editable=False, unique=True,
                                verbose_name='Внутренний номер счета')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата и время создания')
    avatar = models.ImageField(upload_to=get_image_path_for_shop, null=True, blank=True, verbose_name='Аватар магазина')
    slug_name = models.CharField(null=False, unique=True, blank=False, max_length=20, verbose_name='Название для URL')

    def __str__(self):
        return self.name_short

    def create_cred_num(self):
        qs_list = self.get_qs_list('cred_num')
        result_ = ''
        while result_ in qs_list or result_ == '':
            result_ = self.make_result(12)
        return result_

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.cred_num is None or self.cred_num == '':
            self.cred_num = self.create_cred_num()
        return super(ShopBaseModel, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class ProductBaseModel(StringGeneratorHelperMixin, models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Наименование продукта')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class StashBaseModel(StringGeneratorHelperMixin, models.Model):
    article = models.CharField(max_length=15, default='', blank=True, editable=False,
                               unique=True, verbose_name='Артикул')
    cost = models.FloatField(default=0.0, blank=False, verbose_name='Стоимость, в рублях')
    image = models.ImageField(upload_to=get_image_path_for_stash, null=True, blank=True,
                              verbose_name='Изображение товара')
    description = models.TextField(default='', blank=True, verbose_name='Описание', max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Дата создания')

    def __str__(self):
        return self.article

    def create_product_article(self):
        qs_list = self.get_qs_list('article')
        result_ = ''
        while result_ in qs_list or result_ == '':
            result_ = self.make_result(15, 'A')
        return result_

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.article is None or self.article == '':
            self.article = self.create_product_article()
        return super(StashBaseModel, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True
        verbose_name = 'Продукт в магазине'
        verbose_name_plural = 'Продукты в магазине'


class CommentBaseModel(models.Model):
    RATE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rate = models.IntegerField(choices=RATE_CHOICES, blank=False, null=False, verbose_name='Оценка товара')
    caption = models.CharField(max_length=50, blank=False, verbose_name='Заголовок комментария')
    description = models.TextField(max_length=1000, blank=False, verbose_name='Текст комментария')

    class Meta:
        abstract = True
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
