from django.contrib import admin
from User.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('nickname','avatar','gender','openid','QQ','WeChat')
    search_fields = ('nickname','openid')

admin.site.register(user,UserAdmin)
admin.site.register([dashboard,collection_post,DownloadFile_post])