from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from FileSharing_Project import jwt_auth
from Users.serializers import *
from Files.serializers import *


class UserViewSet(ViewSet):

    def jwt_token(self, request):
        jwt_code = jwt_auth.jwt_sys(request).main()
        if jwt_code['is_real'] is not True:
            return True  # if error return true
        request.data['user_id'] = jwt_code['user_id']

    def get_userinfo(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)

    def get_userfile_list(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        queryset = File.objects.filter(user_id=pk)
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def perform_update_userinfo(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers = UserSerializer(instance=user, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)


class CollectionView(APIView):

    def jwt_token(self, request):
        jwt_code = jwt_auth.jwt_sys(request).main()
        if jwt_code['is_real'] is not True:
            return True  # if error return true
        request.data['user_id'] = jwt_code['user_id']

    def get(self, request):
        if self.jwt_token(request): raise PermissionError('Token错误')
        user_id = request.data['user_id']
        idset = CollectionPost.objects.filter(user_id=user_id).values_list('file_id', flat=True)
        queryset = []
        for i in idset:
            if File.objects.get(id=i).exists():
                queryset.extend(File.objects.get(id=i))
        serializers = FileSerializer(instance=queryset, many=True)
        return Response(serializers.data)

    def post(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        data = {
            'user_id': request.data['user_id'],
            'file_id': pk,
        }
        serializer = CollectionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        collection_num = Dashboard.objects.filter(user_id=pk).values('collection_num')[0]['collection_num']
        Dashboard.objects.filter(user_id=pk).update(collection_num=collection_num + 1)
        return Response(serializer.data)

    def delete(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        user_id = request.data['user_id']
        try:
            relation = CollectionPost.objects.filter(user_id=user_id, file_id=pk)
        except CollectionPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        relation.delete()
        collection_num = Dashboard.objects.filter(user_id=user_id).values('collection_num')[0]['collection_num']
        Dashboard.objects.filter(user_id=user_id).update(collection_num=collection_num - 1)
        return Response(status=status.HTTP_200_OK)


class DownloadView(APIView):

    def jwt_token(self, request):
        jwt_code = jwt_auth.jwt_sys(request).main()
        if jwt_code['is_real'] is not True:
            return True  # if error return true
        request.data['user_id'] = jwt_code['user_id']

    def get(self, request):
        if self.jwt_token(request): raise PermissionError('Token错误')
        idset = DownloadFilePost.objects.filter(user_id=request.data['user_id']).values_list('file_id', flat=True)
        queryset = []
        for i in idset:
            if File.objects.get(id=i).exists():
                queryset.extend(File.objects.get(id=i))
        serializers = FileSerializer(instance=queryset, many=True)
        return Response(serializers.data)

    def post(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        try:
            file = File.objects.get(id=pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_id = request.data['user_id']
        if DownloadFilePost.objects.get(user_id=user_id, file_id=pk):
            DownloadFilePost.objects.create(user_id=user_id, file_id=pk)
        download_num = File.objects.filter(id=pk).values('download_num')[0]['download_num']
        File.objects.filter(id=pk).update(download_num=download_num + 1)
        DownloadFile_num = Dashboard.objects.filter(id=user_id).values('DownloadFile_num')[0]['DownloadFile_num']
        Dashboard.objects.filter(id=user_id).update(DownloadFile_num=DownloadFile_num + 1)
        serializer = FileSerializer(instance=file)
        return Response(serializer.data)

    def delete(self, request, pk):
        if self.jwt_token(request): raise PermissionError('Token错误')
        user_id = request.data['user_id']
        try:
            relation = CollectionPost.objects.filter(user_id=user_id, file_id=pk)
        except CollectionPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        relation.delete()
        DownloadFile_num = Dashboard.objects.filter(id=user_id).values('DownloadFile_num')[0]['DownloadFile_num']
        Dashboard.objects.filter(id=user_id).update(DownloadFile_num=DownloadFile_num - 1)
        return Response(status=status.HTTP_200_OK)
