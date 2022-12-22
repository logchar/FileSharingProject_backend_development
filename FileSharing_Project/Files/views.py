from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
import jieba

from FileSharing_Project import jwt_auth
from Files.osssys import *
from Files.serializers import *


class FileViewSet(ViewSet):

    def jwt_token(self, request):
        jwt_code = jwt_auth.jwt_sys(request).main()
        if jwt_code['is_real'] is not True:
            return True  # if error return true
        request.data['user'] = jwt_code['user_id']

    def get_list(self, request):
        if self.jwt_token(request): raise PermissionError('Token错误')
        queryset = File.objects.all()
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def get_detail(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        try:
            file = File.objects.get(id=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FileSerializer(instance=file)
        return Response(serializer.data)

    def perform_upload(self, request):
        if self.jwt_token(request): raise PermissionError('Token错误')
        data = request.data
        data['suffix'] = data['name'].split('.')[-1]
        fileobj = request.File[data['name']]
        data['size'] = fileobj.size / 1024.0
        data['download_num'] = 0
        file_name = str(data['user_id']) + "_" + data['name'] + "_" + str(File.objects.all().count()) + "." + data['suffix']
        is_update = Oss().upload_file(filename=file_name, file=fileobj.read())
        if is_update is False:
            raise PermissionError('上传失败')
        data['name'] = file_name
        data['address'] = Oss().get_url(file_name)
        upload_num = Dashboard.objects.filter(user_id=request.data['user_id']).values('UploadFile_num')[0]['UploadFile_num']
        Dashboard.objects.filter(user_id=request.data['user_id']).update(UploadFile_num=upload_num + 1)
        serializer = FileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def perform_change(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        try:
            file = File.objects.get(id=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['suffix'] = data['file'].name.split('.')[-1]
        data['size'] = data['file'].size / 1024.0 / 1024.0
        file_name = str(data['user_id']) + "_" + data['name'] + "_" + str(File.objects.all().count()) + "." + data['suffix']
        is_updata = Oss().upload_file(filename=file_name, file=data['file'].read())
        if is_updata is False:
            raise PermissionError('上传失败')
        data['address'] = Oss().get_url(file_name)
        serializer = FileSerializer(instance=file,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def perform_delete(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        try:
            file = File.objects.get(id=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        name = file.values('name')[0]['name']
        is_delete = Oss().delete_file(name)
        if is_delete is False: raise PermissionError('Oss删除失败')
        file.delete()
        upload_num = Dashboard.objects.filter(user_id=request.data['user_id']).values('UploadFile_num')[0]['UploadFile_num']
        Dashboard.objects.filter(user_id=request.data['user_id']).update(UploadFile_num=upload_num - 1)
        download_num = File.objects.filter(id=pk).values('download_num')[0]['download_num']
        File.objects.filter(id=pk).update(download_num=download_num - 1)
        return Response(status=status.HTTP_200_OK)

    def perform_search(self, request):
        if self.jwt_token(request): raise PermissionError('Token错误')
        file_list_id = []
        search_content = request.data['search_content']
        # 优先全字段匹配
        bestfiles_id = File.objects.filter(name__icontains=search_content).values_list('id', flat=True)
        file_list_id.extend(bestfiles_id)
        # 字段拆分匹配
        word_list = jieba.cut(search_content, cut_all=True)
        for word in word_list:
            suggestfiles_id = File.objects.filter(name__icontains=word).values_list('id', flat=True)
            file_list_id.extend(suggestfiles_id)
        file_list_id = list(set(file_list_id))  # 搜索去重
        file_list = []
        for i in file_list_id:
            file_list.extend(File.objects.get(id=i))
        serializer = FileSerializer(instance=file_list, many=True)
        return Response(serializer.data)

