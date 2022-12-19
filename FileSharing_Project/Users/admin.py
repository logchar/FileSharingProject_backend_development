from django.contrib import admin
from Users.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'avatar', 'openid', 'QQ', 'WeChat', 'create_time', 'update_time')
    search_fields = ('nickname', 'openid')


admin.site.register(User, UserAdmin)
admin.site.register(Dashboard)
