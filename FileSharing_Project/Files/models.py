from django.db import models

from Users.models import User, Dashboard


class File(models.Model):  # 文件相关信息表
    user = models.ForeignKey(User, verbose_name='上传者id', on_delete=models.CASCADE)
    filename = models.CharField(verbose_name='文件上传名', max_length=75, blank=True, null=True)
    name = models.CharField(verbose_name='文件原名', max_length=75)
    suffix = models.CharField(verbose_name='后缀名', max_length=15)
    address = models.URLField(verbose_name='资源路径', max_length=200)
    size = models.CharField(verbose_name='文件大小', max_length=30)
    department = models.CharField(verbose_name='学院', max_length=15, blank=True, null=True)
    subject = models.CharField(verbose_name='学科', max_length=15, blank=True, null=True)
    readme = models.CharField(verbose_name='简介', max_length=300, blank=True, null=True)
    download_num = models.IntegerField(verbose_name='下载量', default=0, blank=True, null=True)
    auth_name = models.CharField(verbose_name='上传者昵称', max_length=30)


class CollectionPost(models.Model):  # 收藏文件映射
    user = models.ForeignKey(User, verbose_name='用户id', on_delete=models.CASCADE)
    file = models.ForeignKey(File, verbose_name='收藏文件id', on_delete=models.CASCADE)


class DownloadFilePost(models.Model):  # 下载文件映射 用于删除下载记录
    user = models.ForeignKey(User, verbose_name='用户id', on_delete=models.CASCADE)
    file = models.ForeignKey(File, verbose_name='下载文件id', on_delete=models.CASCADE)
