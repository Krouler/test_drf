from rest_framework import serializers

from marketplace.models import Shop, ConfidentialInfoShop


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
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='shop-detail', read_only=True, lookup_field='slug_name')
    conf_data = serializers.SerializerMethodField('get_conf_data')

    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('cred_num',)

    def get_conf_data(self, obj):
        confdata = ConfidentialInfoShop.objects.get(shop=obj)
        return ShopConfData(confdata).data

