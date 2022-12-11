from django.db import models

# Create your models here.


class File(models.Model):  # 文件相关信息表
    auth_id = models.BigIntegerField(verbose_name='上传者id', default=0)
    name = models.CharField(verbose_name='文件名', max_length=75)
    suffix = models.CharField(verbose_name='后缀名', max_length=75)
    address = models.URLField(verbose_name='资源路径', max_length=200)
    size = models.CharField(verbose_name='文件大小', max_length=30)
    department = models.CharField(verbose_name='学院', max_length=30, blank=True, null=True)
    subject = models.CharField(verbose_name='学科', max_length=30, blank=True, null=True)
    readme = models.CharField(verbose_name='简介', max_length=300, blank=True, null=True)
    download_num = models.IntegerField(verbose_name='下载量', default=0)
    auth_name = models.CharField(verbose_name='上传者昵称', max_length=50)
