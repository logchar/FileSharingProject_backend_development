from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pathlib import Path

from Post.models import File
from User.models import *
from FileSharing_Project import jwt_auth

# Create your views here.


@csrf_exempt
def get_user_info(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            user_id = jwt_code['user_id']
            user_obj = User.objects.filter(id=user_id).values('id', 'nickname', 'gender', 'openid', 'QQ', 'WeChat')[0]
            dashboard_details = Dashboard.objects.filter(user__id=user_id).values('collection_num', 'UploadFile_num', 'DownloadFile_num')[0]
            user_info = dict( user_obj, **dashboard_details )
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": user_info
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def get_avatar(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            user_id = jwt_code['user_id']
            pic_url = "/static/media_pics/"
            if User.objects.filter(id=user_id).exists():
                pic_name = User.objects.filter(id=user_id).values('avatar')[0]['avatar']
                pic_url = pic_url + pic_name + "_" + str(user_id)
            else:
                pic_url = pic_url + "DefaultAvatar.png"
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": pic_url,
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def get_collection_list(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            user_id = jwt_code['user_id']
            post_list = []
            collection_list = CollectionPost.objects.filter(userID=user_id)
            if collection_list.exists():
                post_id_list = list(collection_list.values_list('fileID', flat=True))
                for i in range(len(post_id_list)):
                    post_id = int(post_id_list[i])
                    if File.objects.filter(id=post_id).exists():
                        post_obj = File.objects.filter(id=post_id).values('id', 'auth_id', 'name', 'suffix', 'address', 'size', 'department', 'subject', 'readme', 'download_num', 'auth_name')[0]
                        post_list.append(post_obj)
                    else:
                        collection_num = Dashboard.objects.filter(user=user_id).values('collection_num')[0]['collection_num']
                        Dashboard.objects.filter(user=user_id).update(collection_num=collection_num-1)
                        CollectionPost.objects.filter(userID=user_id, fileID=post_id).delete()
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": post_list
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def get_upload_list(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            user_id = jwt_code['user_id']
            post_list = []
            upload_list = File.objects.filter(auth_id=user_id)
            if upload_list.exists():
                post_id_list = list(upload_list.values_list('id', flat=True))
                for i in range(len(post_id_list)):
                    post_id = int(post_id_list[i])
                    post_obj = File.objects.filter(id=post_id).values('id', 'auth_id', 'name', 'suffix', 'address', 'size', 'department', 'subject', 'readme', 'download_num', 'auth_name')[0]
                    post_list.append(post_obj)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": post_list
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def get_download_list(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            user_id = jwt_code['user_id']
            post_list = []
            download_list = DownloadFilePost.objects.filter(userID=user_id)
            if download_list.exists():
                post_id_list = list(DownloadFilePost.objects.values_list('fileID', flat=True))
                for i in range(len(post_id_list)):
                    post_id = int(post_id_list[i])
                    if File.objects.filter(id=post_id).exists():
                        post_obj = File.objects.filter(id=post_id).values('id', 'auth_id', 'name', 'suffix', 'address','size', 'department', 'subject', 'readme','download_num', 'auth_name')[0]
                        post_list.append(post_obj)
                    else:
                        download_num = Dashboard.objects.filter(user=user_id).values('DownloadFile_num')[0]['DownloadFile_num']
                        Dashboard.objects.filter(user=user_id).update(DownloadFile_num=download_num - 1)
                        DownloadFilePost.objects.filter(userID=user_id, fileID=post_id).delete()
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": post_list
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def get_file_list(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            file_list = []
            start_id = request.GET.get('start_id')
            for i in range(int(start_id), int(start_id)+10):
                if File.objects.filter(id=i).exists():
                    file_obj = File.objects.filter(id=i).values('id', 'auth_id', 'name', 'suffix', 'address', 'size', 'department', 'subject', 'readme', 'download_num', 'auth_name')[0]
                    file_list.append(file_obj)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": file_list
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def updata_avatar(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'POST':
            avatar = request.FILES.get('avatar')
            user_id = jwt_code['user_id']
            pic_url = str(Path(__file__).resolve().parent.parent) + "/static/media_pics/" + str(avatar.name) + "_" + str(user_id)
            with open(pic_url, 'wb') as f:
                for content in avatar.chunks():
                    f.write(content)
            User.objects.filter(id=user_id).update(avatar=avatar)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": True,
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def updata_nickname(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            nickname = request.GET.get('nickname')
            user_id = jwt_code['user_id']
            User.objects.filter(id=user_id).update(nickname=nickname)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": True,
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def updata_qq(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            QQ = request.GET.get('QQ')
            user_id = jwt_code['user_id']
            User.objects.filter(id=user_id).update(QQ=QQ)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": True,
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def updata_wechat(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            WeChat = request.GET.get('WeChat')
            user_id = jwt_code['user_id']
            User.objects.filter(id=user_id).update(WeChat=WeChat)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": True,
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "",
                "msg": "请求失败，方法错误",
                "debug": debug_msg,
                "data": False
            }
            return JsonResponse(response)
    else:
        response = {
            "code": "A0205",
            "msg": "请求失败，token错误",
            "data": False
        }
        return JsonResponse(response)
