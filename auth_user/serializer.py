from rest_framework import serializers

from auth_user.models import Profile


class RetrieveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile

