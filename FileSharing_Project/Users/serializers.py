from rest_framework import serializers

from Users.models import *
from Files.models import CollectionPost, DownloadFilePost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'avatar', 'openid', 'QQ', 'WeChat']


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionPost
        fields = '__all__'


class DownloadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadFilePost
        fields = '__all__'
