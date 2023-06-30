from rest_framework import serializers

from marketplace.models import Shop, ConfidentialInfoShop, Product


class ShopConfData(serializers.ModelSerializer):
    class Meta:
        model = ConfidentialInfoShop
        fields = '__all__'
        read_only_fields = ('shop', 'balance')


class ShopSerializerForCustomer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='shop-detail', read_only=True, lookup_field='slug_name')
    slug_name = serializers.CharField(read_only=True)

    class Meta:
        model = Shop
        exclude = ('balance', )


class ShopSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='shop-detail', read_only=True, lookup_field='slug_name')
    conf_data = serializers.SerializerMethodField('get_conf_data')

    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('cred_num', 'balance')

    def get_conf_data(self, obj):
        confdata = ConfidentialInfoShop.objects.get(shop=obj)
        return ShopConfData(confdata).data


# class ProductSerializerForCustomer(serializers.HyperlinkedModelSerializer):
#     url = serializers.HyperlinkedIdentityField()
#
#     class Meta:
#         model = Product
#         fields = '__all__'

