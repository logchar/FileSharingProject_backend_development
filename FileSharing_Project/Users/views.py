from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from FileSharing_Project.jwt_auth import jwt_sys
from Users.serializers import *
from Files.serializers import *


class UserViewSet(ViewSet):

    def get_userinfo(self, request):
        user_id = jwt_sys(request).main()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)

    def get_userfile_list(self, request):
        user_id = jwt_sys(request).main()
        queryset = File.objects.filter(user_id=user_id)
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def perform_update_userinfo(self, request):
        user_id = jwt_sys(request).main()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class CollectionView(APIView):

    def get(self, request):
        user_id = jwt_sys(request).main()
        idset = CollectionPost.objects.filter(user_id=user_id).values_list('file_id', flat=True)
        queryset = File.objects.filter(id__in=idset)
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        user_id = jwt_sys(request).main()
        if CollectionPost.objects.filter(user_id=user_id, file_id=pk) is None:
            CollectionPost.objects.create(user_id=user_id, file_id=pk)
            updata_dashboard(user_id, "collection_num", 1)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user_id = jwt_sys(request).main()
        try:
            relation = CollectionPost.objects.filter(user_id=user_id, file_id=pk)
        except CollectionPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        relation.delete()
        updata_dashboard(user_id, "collection_num", -1)
        return Response(status=status.HTTP_200_OK)


class DownloadView(APIView):

    def get(self, request):
        user_id = jwt_sys(request).main()
        idset = DownloadFilePost.objects.filter(user_id=user_id).values_list('file_id', flat=True)
        queryset = File.objects.filter(id__in=idset)
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        user_id = jwt_sys(request).main()
        relation = DownloadFilePost.objects.get(user_id=user_id, file_id=pk)
        if relation is None:
            relation = DownloadFilePost.objects.create(user_id=user_id, file_id=pk)
            updata_download_num(pk, 1)
            updata_dashboard(user_id, "DownloadFile_num", 1)
        serializer = DownloadFileSerializer(instance=relation)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user_id = jwt_sys(request).main()
        try:
            relation = CollectionPost.objects.filter(user_id=user_id, file_id=pk)
        except CollectionPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        relation.delete()
        updata_dashboard(user_id, "DownloadFile_num", -1)
        return Response(status=status.HTTP_200_OK)
