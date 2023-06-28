from rest_framework import serializers

from marketplace.models import Shop


class ShopSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='shop-detail', read_only=True, lookup_field='slug_name')

    class Meta:
        model = Shop
        fields = '__all__'


class ShopSerializerForCustomer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='shop-detail', read_only=True, lookup_field='slug_name')

    class Meta:
        model = Shop
        fields = ('name', 'name_short', 'inn', 'ceo', 'cred_num', 'created_at', 'avatar', 'url')
