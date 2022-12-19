from django.contrib import admin
from Files.models import *

# Register your models here.


class FileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'suffix', 'address', 'size', 'department', 'subject', 'readme', 'download_num', 'auth_name')
    search_fields = ('name', 'user_id')

admin.site.register(File,FileAdmin)
admin.site.register([CollectionPost, DownloadFilePost])