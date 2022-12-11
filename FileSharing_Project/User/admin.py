from django.contrib import admin
from User.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('nickname','avatar','gender','openid','QQ','WeChat')
    search_fields = ('nickname','openid')

admin.site.register(User,UserAdmin)
admin.site.register([Dashboard,CollectionPost,DownloadFilePost])