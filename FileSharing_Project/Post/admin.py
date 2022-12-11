from django.contrib import admin
from Post.models import *

# Register your models here.


class FileAdmin(admin.ModelAdmin):
    list_display = ('auth_id', 'name', 'suffix', 'address', 'size', 'department', 'subject', 'readme', 'download_num', 'auth_name')
    search_fields = ('name', 'auth_id')

admin.site.register(file,FileAdmin)