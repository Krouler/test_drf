from abc import ABC

from django.contrib.auth.models import User
from rest_framework import serializers

from auth_user.models import Profile


class RetrieveUserSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField()

    class Meta:
        model = Profile
        fields = ('invite_code', 'id', 'last_name', 'first_name', 'second_name', 'born')
        extra_kwargs = {
            'invite_code': {'required': True},
            'born': {'required': False}
        }
        read_only_fields = ('first_name', 'last_name', 'second_name')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('balance', 'invite_code', 'user')


class SelfProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('username', 'balance', 'invite_code', 'user')

    def get_username(self, obj):
        return obj.user.username


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', )


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True, max_length=100)
    new_password = serializers.CharField(write_only=True, required=True, max_length=100)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')