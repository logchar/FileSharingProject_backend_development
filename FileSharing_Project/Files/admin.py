from django.contrib import admin
from Files.models import *

# Register your models here.


class FileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'suffix', 'address', 'size', 'department', 'subject', 'readme', 'download_num')
    search_fields = ('name', 'user')

admin.site.register(File,FileAdmin)
admin.site.register([CollectionPost, DownloadFilePost])