from rest_framework import serializers

from Files.models import *

class FileSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(label='上传者id', read_only=True)
    name = serializers.CharField(label='文件名', max_length=75)
    suffix = serializers.CharField(label='后缀名', max_length=15)
    address = serializers.URLField(label='资源路径', max_length=200)
    size = serializers.CharField(label='文件大小', max_length=30)
    department = serializers.CharField(label='学院', max_length=15, required=False)
    subject = serializers.CharField(label='学科', max_length=15, required=False)
    readme = serializers.CharField(label='简介', max_length=300, required=False)
    download_num = serializers.IntegerField(label='下载量', required=False)
    auth_name = serializers.CharField(label='上传者昵称', max_length=30)

    def validate(self, attrs):
        if attrs['size'] > 512:
            serializers.ValidationError('文件过大')
        return attrs

    def create(self, validated_data):
        newbook = File.objects.create(**validated_data)
        return newbook

    def update(self, instance, validated_data):
        instance.user_id = validated_data['user_id']
        instance.name = validated_data['name']
        instance.suffix = validated_data['suffix']
        instance.address = validated_data['address']
        instance.size = validated_data['size']
        instance.auth_name = validated_data['auth_name']
        if validated_data['download_num'] is not None:
            instance.download_num = validated_data['download_num']
        if validated_data['department'] is not None:
            instance.department = validated_data['department']
        if validated_data['subject'] is not None:
            instance.subject = validated_data['subject']
        if validated_data['readme'] is not None:
            instance.readme = validated_data['readme']
        instance.save()
        return instance
