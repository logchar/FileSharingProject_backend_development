from django.db import models
from PIL import Image


class User(models.Model):  # 用户信息
    nickname = models.CharField(verbose_name='昵称', max_length=30)
    avatar = models.ImageField(verbose_name='头像', blank=True, null=True, upload_to='avatar')
    openid = models.CharField(verbose_name='openid', max_length=30)
    QQ = models.CharField(verbose_name='QQ', max_length=20, blank=True, null=True)
    WeChat = models.CharField(verbose_name='WeChat', max_length=30, blank=True, null=True)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)


class Dashboard(models.Model):  # 用户的文件数据表
    user = models.ForeignKey(User, verbose_name='对应用户id', on_delete=models.CASCADE)
    collection_num = models.PositiveIntegerField(verbose_name='收藏数', default=0)
    UploadFile_num = models.PositiveIntegerField(verbose_name='上传文件数', default=0)
    DownloadFile_num = models.PositiveIntegerField(verbose_name='下载文件数', default=0)
