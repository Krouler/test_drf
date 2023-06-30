from django.contrib.auth.models import User
from django.db import models

from marketplace.models_base import StringGeneratorHelperMixin


def get_image_path_for_stash(instance, filename):
    return 'users/{0}/avatar/{1}'.format(instance.user.username, filename)


class Profile(StringGeneratorHelperMixin, models.Model):
    SEX_CHOICE = [
        ('Male', 'Мужчина'),
        ('Female', 'Женщина')
    ]
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0, blank=True, verbose_name='Баланс, в рублях')
    second_name = models.CharField(max_length=25, blank=True, verbose_name='Отчество')
    sex = models.CharField(choices=SEX_CHOICE, blank=False, verbose_name='Пол')
    avatar = models.ImageField(upload_to=get_image_path_for_stash, blank=True, verbose_name='Аватар')
    invite_code = models.CharField(default='', max_length=12, blank=True, verbose_name='Личный код')

    def generate_invite_code(self):
        qs_list = self.get_qs_list('invite_code')
        result_ = ''
        while result_ in qs_list or result_ == '':
            result_ = self.make_result(12, 'INV')
        return result_

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.invite_code is None or self.invite_code == '':
            self.invite_code = self.generate_invite_code()
        return super(Profile, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.user.username
