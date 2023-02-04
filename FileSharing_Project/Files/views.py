from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Q
import jieba

from FileSharing_Project.jwt_auth import jwt_sys
from Files.osssys import *
from Files.serializers import *
from celery_tasks.upload.tasks import UploadFile


class FileViewSet(ViewSet):

    def get_list(self, request, pk):
        jwt_sys(request).main()
        start_id = pk
        queryset = File.objects.filter(id__range=[start_id, start_id+9])
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def get_detail(self, request, pk):
        jwt_sys(request).main()
        file = File.objects.get(id=pk)
        serializer = FileSerializer(instance=file)
        return Response(serializer.data)

    def perform_upload(self, request, pk):
        user_id = jwt_sys(request).main()
        data = request.data
        fileobj = request.FILES[data['name']]
        name = str(user_id) + "_" + str(File.objects.all().count()) + "_" + fileobj.name
        # is_update = Oss().upload_file(filename=name, file=fileobj.read())
        # if is_update is False:
        #     raise PermissionError('上传失败')
        UploadFile.delay(name, fileobj)
        datadict = {
            'name': name,
            'filename': data['filename'],
            'department': data['department'],
            'subject': data['subject'],
            'readme': data['readme'],
            'upload_time': data['upload_time'],
            'user': User.objects.get(id=user_id),
            'suffix': data['name'].split('.')[-1],
            'address': Oss().get_url(name),
            'size': str(int(fileobj.size / 1024.0 + 0.5)) + 'KB',
            'download_num': 0,
        }
        updata_dashboard(user_id, "UploadFile_num", 1)
        File.objects.create(**datadict)
        return Response(status=status.HTTP_200_OK)

    def perform_change(self, request, pk):  # 允许修改文件名，简介，所属学院和学科
        jwt_sys(request).main()
        file = File.objects.filter(id=pk)
        serializer = FileSerializer(instance=request.data)
        file.update(**serializer.data)
        return Response(status=status.HTTP_200_OK)

    def perform_delete(self, request, pk):
        user_id = jwt_sys(request).main()
        file = File.objects.filter(id=pk)
        is_delete = Oss().delete_file(file.values('name')[0]['name'])
        if is_delete is False:
            raise PermissionError('Oss删除失败')
        file.delete()
        updata_dashboard(user_id, "UploadFile_num", -1)
        updata_download_num(pk, -1)
        return Response(status=status.HTTP_200_OK)

    def perform_search(self, request):
        jwt_sys(request).main()
        file_list_id = []
        search_content = request.data['search_content']
        # 优先全字段匹配
        bestfiles_id = File.objects.filter(
            Q(filename__icontains=search_content) |
            Q(subject__icontains=search_content) |
            Q(department__icontains=search_content)
        ).values_list('id', flat=True)
        file_list_id.extend(bestfiles_id)
        # 字段拆分匹配
        word_list = jieba.cut(search_content, cut_all=True)
        for word in word_list:
            suggestfiles_id = File.objects.filter(filename__icontains=word).values_list('id', flat=True)
            file_list_id.extend(suggestfiles_id)
        file_list_id = list(set(file_list_id))  # 搜索去重
        file_list = File.objects.filter(id__in=file_list_id)
        serializer = FileSerializer(instance=file_list, many=True)
        return Response(serializer.data)

