from rest_framework import serializers

from Users.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'openid', 'QQ', 'WeChat']


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'
