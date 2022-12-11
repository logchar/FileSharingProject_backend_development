from django.db import models

# Create your models here.


class User(models.Model):  # 用户信息
    nickname = models.CharField(verbose_name='昵称', max_length=30)
    avatar = models.ImageField(verbose_name='头像', blank=True, null=True, upload_to='avatar')
    gender = models.CharField(verbose_name='性别', max_length=10, blank=True, null=True)
    openid = models.CharField(verbose_name='openid', max_length=30)
    QQ = models.CharField(verbose_name='QQ', max_length=50, blank=True, null=True)
    WeChat = models.CharField(verbose_name='WeChat', max_length=50, blank=True, null=True)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)


class Dashboard(models.Model):  # 用户的文件数据表
    user = models.ForeignKey(User, verbose_name='对应用户id', on_delete=models.CASCADE)
    collection_num = models.PositiveIntegerField(verbose_name='收藏数', default=0)
    UploadFile_num = models.PositiveIntegerField(verbose_name='上传文件数', default=0)
    DownloadFile_num = models.PositiveIntegerField(verbose_name='下载文件数', default=0)


class CollectionPost(models.Model):  # 收藏文件映射
    userID = models.CharField(verbose_name='用户id', max_length=30, default='')
    fileID = models.CharField(verbose_name='收藏文件id', max_length=30)


class DownloadFilePost(models.Model):  # 下载文件映射 用于删除下载记录
    userID = models.CharField(verbose_name='用户id', max_length=30, default='')
    fileID = models.CharField(verbose_name='下载文件id', max_length=30)
