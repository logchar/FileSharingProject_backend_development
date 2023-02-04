from pathlib import Path

from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from FileSharing_Project.jwt_auth import jwt_sys
from Users.serializers import *
from Files.serializers import *


class UserViewSet(ViewSet):

    def get_avatar_url(self, user_id):
        pic_url = "static/media_pics/"
        pic_name = User.objects.filter(id=user_id).values('avatar')[0]['avatar']
        if pic_name is not "":
            pic_url = pic_url + str(user_id) + "_" + pic_name
        else:
            pic_url = pic_url + "DefaultAvatar.png"
        return pic_url

    def get_userinfo(self, request):
        user_id = jwt_sys(request).main()
        user = User.objects.filter(id=user_id)[0]
        serializer = UserSerializer(instance=user)
        datadict = dict(serializer.data)
        datadict.update({'avatar': self.get_avatar_url(user_id)})
        return Response(datadict)

    def get_other_userinfo(self, request, pk):
        jwt_sys(request).main()
        user = User.objects.filter(id=pk)[0]
        serializer = UserSerializer(instance=user)
        datadict = dict(serializer.data)
        datadict.update({'avatar': self.get_avatar_url(pk)})
        datadict.pop('openid')
        return Response(datadict)

    def get_userfile_list(self, request):
        user_id = jwt_sys(request).main()
        queryset = File.objects.filter(user_id=user_id)
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def perform_update_userinfo(self, request):
        user_id = jwt_sys(request).main()
        user = User.objects.filter(id=user_id)
        serializer = UserSerializer(instance=request.data)
        user.update(**serializer.data)
        return Response(status=status.HTTP_200_OK)

    def perform_update_avatar(self, request, pk):
        user_id = jwt_sys(request).main()
        user = User.objects.filter(id=user_id)
        for avatar in request.FILES.values():
            pic_url = str(Path(__file__).resolve().parent.parent) + "/static/media_pics/" + str(user_id) + "_" + str(avatar.name)
            with open(pic_url, 'wb') as f:
                for content in avatar.chunks():
                    f.write(content)
            user.update(avatar=avatar)
        return Response(status=status.HTTP_200_OK)


class CollectionView(APIView):

    def get(self, request, pk):
        user_id = jwt_sys(request).main()
        idset = CollectionPost.objects.filter(user_id=user_id).values_list('file_id', flat=True)
        queryset = File.objects.filter(id__in=idset)
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        user_id = jwt_sys(request).main()
        CollectionPost.objects.create(user_id=user_id, file_id=pk)
        updata_dashboard(user_id, "collection_num", 1)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user_id = jwt_sys(request).main()
        relation = CollectionPost.objects.filter(user_id=user_id, file_id=pk)
        relation.delete()
        updata_dashboard(user_id, "collection_num", -1)
        return Response(status=status.HTTP_200_OK)


class DownloadView(APIView):

    def get(self, request, pk):
        user_id = jwt_sys(request).main()
        idset = DownloadFilePost.objects.filter(user_id=user_id).values_list('file_id', flat=True)
        queryset = File.objects.filter(id__in=idset)
        serializer = FileSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        user_id = jwt_sys(request).main()
        DownloadFilePost.objects.create(user_id=user_id, file_id=pk)
        updata_download_num(pk, 1)
        updata_dashboard(user_id, "DownloadFile_num", 1)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user_id = jwt_sys(request).main()
        relation = CollectionPost.objects.filter(user_id=user_id, file_id=pk)
        relation.delete()
        updata_dashboard(user_id, "DownloadFile_num", -1)
        return Response(status=status.HTTP_200_OK)
