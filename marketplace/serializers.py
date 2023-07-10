from rest_framework import serializers

from marketplace.models import Shop, ConfidentialInfoShop, Product, Stash


class ShopConfData(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField('get_employee_code_from_id')

    class Meta:
        model = ConfidentialInfoShop
        fields = '__all__'
        read_only_fields = ()

    def get_employee_code_from_id(self, obj):
        imp = {}
        employee = obj.employee.all()
        for i in employee:
            imp[i.id] = {'invite_code': i.profile.invite_code,
                         'first_name': i.profile.first_name,
                         'last_name': i.profile.last_name}
        return imp


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


class ShopInfoInProduct(serializers.ModelSerializer):

    class Meta:
        model = Stash
        fields = ('shop', 'cost', 'count')


class ProductSerializerForCustomer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', read_only=True)
    in_shops = serializers.SerializerMethodField('get_shops')

    class Meta:
        model = Product
        exclude = ('shop',)

    def get_shops(self, obj):
        qs = Stash.objects.select_related('shop', 'product').only('shop', 'cost', 'count', 'product').filter(product=obj)
        if len(qs) > 0:
            return ShopInfoInProduct(qs).data
        return {}


class InviteUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfidentialInfoShop
        fields = ('employee', )
