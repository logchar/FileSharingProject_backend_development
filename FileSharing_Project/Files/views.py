from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Q
import jieba

from FileSharing_Project.jwt_auth import jwt_sys
from Files.osssys import *
from Files.serializers import *


class FileViewSet(ViewSet):

    def get_list(self, request):
        jwt_sys(request).main()
        start_id = request.data['start_id']
        queryset = File.objects.filter(id__range=[start_id, start_id+9])
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def get_detail(self, request, pk):
        jwt_sys(request).main()
        try:
            file = File.objects.get(id=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FileSerializer(instance=file)
        return Response(serializer.data)

    def perform_upload(self, request):
        user_id = jwt_sys(request).main()
        data = request.data
        fileobj = request.File[data['name']]
        file_name = str(user_id) + "_" + data['name'] + "_" + str(File.objects.all().count())
        is_update = Oss().upload_file(filename=file_name, file=fileobj.read())
        if is_update is False:
            raise PermissionError('上传失败')
        backend_data = {
            'user': user_id,
            'suffix': data['name'].split('.')[-1],
            'size': str(int(fileobj.size / 1024.0)) + 'KB',
            'download_num': 0,
            'name': file_name,
            'address': Oss().get_url(file_name),
        }
        data.update(backend_data)
        updata_dashboard(user_id, "UploadFile_num", 1)
        serializer = FileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def perform_change(self, request, pk):  # 允许修改文件名，简介，所属学院和学科
        jwt_sys(request).main()
        try:
            file = File.objects.get(id=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = FileSerializer(instance=file, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def perform_delete(self, request, pk):
        user_id = jwt_sys(request).main()
        try:
            file = File.objects.filter(id=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
            Q(name__icontains=search_content) |
            Q(subject__icontains=search_content) |
            Q(department__icontains=search_content)
        ).values_list('id', flat=True)
        file_list_id.extend(bestfiles_id)
        # 字段拆分匹配
        word_list = jieba.cut(search_content, cut_all=True)
        for word in word_list:
            suggestfiles_id = File.objects.filter(
                Q(name__icontains=word) |
                Q(filename__icontains=word)
            ).values_list('id', flat=True)
            file_list_id.extend(suggestfiles_id)
        file_list_id = list(set(file_list_id))  # 搜索去重
        file_list = File.objects.filter(id__in=file_list_id)
        serializer = FileSerializer(instance=file_list, many=True)
        return Response(serializer.data)

