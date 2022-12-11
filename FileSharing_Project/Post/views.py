### from Misc.models import search_history
import json
import urllib
import jieba

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Post.models import *
from User.models import *
from FileSharing_Project import jwt_auth
from Post.osssys import *

# Create your views here.


@csrf_exempt
def uploads_file(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'POST':
            file_obj = request.FILES.get('file')
            filename = request.POST.get('filename')
            department = request.POST.get('department')
            subject = request.POST.get('subject')
            readme = request.POST.get('readme')
            suffix = file_obj.name.split('.')[-1]
            size = file_obj.size / 1024.0 / 1024.0
            user_id = jwt_code['user_id']
            auth_name = user.objects.filter(id=user_id).values('nickname')[0]['nickname']
            filedb_obj = file.objects.create(auth_id=user_id, name=filename, suffix=suffix, size=size, readme=readme, department=department, subject=subject, auth_name=auth_name)
            filedb_obj_id = filedb_obj.id
            is_updata = oss().upload_file(file_obj.read(), user_id, filename, filedb_obj_id,suffix)
            if is_updata is True:
                address = oss().get_url(str(user_id)+"_"+filename+"_"+str(filedb_obj_id)+"."+suffix)
                file.objects.filter(id=filedb_obj_id).update(address=address)
                file_num = dashboard.objects.filter(user=user_id).values('UploadFile_num')[0]['UploadFile_num']
                file_num = int(file_num)+1
                dashboard.objects.filter(user=user_id).update(UploadFile_num=file_num)
                response = {
                    "code": "00000",
                    "msg": "请求成功",
                    "data": True
                }
                return JsonResponse(response)
            else:
                file.objects.filter(id=filedb_obj_id).delete()
                response = {
                    "code": "",
                    "msg": "请求失败，文件上传错误",
                    "data": False
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
            "msg": "请求失败，token超时或出现错误",
            "data": False
        }
        return JsonResponse(response)


@csrf_exempt
def delete_file(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            user_id = jwt_code['user_id']
            file_id = request.GET.get('file_id')
            obj = file.objects.filter(id=file_id)
            if obj.exists():
                name = obj.values('name')[0]['name']
                is_delete = oss().delete_file(name)
                if is_delete is True:
                    obj.delete()
                    file_num = dashboard.objects.filter(user=user_id).values('UploadFile_num')[0]['UploadFile_num']-1
                    if file_num < 0:
                        file_num = 0
                    dashboard.objects.filter(user=user_id).update(UploadFile_num=file_num)
                    response = {
                        "code": "00000",
                        "msg": "请求成功",
                        "data": True
                    }
                    return JsonResponse(response)
                else:
                    response = {
                        "code": "",
                        "msg": "请求失败，未删除成功",
                        "data": False
                    }
                    return JsonResponse(response)
            else:
                response = {
                    "code": "",
                    "msg": "请求失败，无此文件",
                    "debug": "file_id=" + str(file_id),
                    "data": False
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
def collect_file(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            user_id = jwt_code['user_id']
            file_id = request.GET.get('file_id')
            collection_post.objects.create(userID=user_id,fileID=file_id)
            file_num = dashboard.objects.filter(user_id=user_id).values('collection_num')[0]['collection_num']
            file_num = file_num+1
            dashboard.objects.filter(user_id=user_id).update(collection_num=file_num)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": True
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
def collection_delect(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            user_id = jwt_code['user_id']
            file_id = request.POST.get('file_id')
            relation_obj = collection_post.objects.filter(userID=user_id,fileID=file_id)
            relation_obj.delete()
            file_num = dashboard.objects.filter(user_id=user_id).values('collection_num')[0]['collection_num']
            if file_num == 0:
                file_num = 1
            file_num = file_num-1
            dashboard.objects.filter(user_id=user_id).update(collection_num=file_num)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": True
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
def download_file(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            user_id = jwt_code['user_id']
            file_id = request.GET.get('file_id')
            file_url = file.objects.filter(id=file_id).values('address')[0]['address']
            file_num = dashboard.objects.filter(user_id=user_id).values('DownloadFile_num')[0]['DownloadFile_num']
            file_num = file_num + 1
            dashboard.objects.filter(user_id=user_id).update(DownloadFile_num=file_num)
            file_download_num = file.objects.filter(id=file_id).values('download_num')[0]['download_num']
            file_download_num = file_download_num + 1
            file.objects.filter(id=file_id).update(download_num=file_download_num)
            DownloadFile_post.objects.create(userID=user_id, fileID=file_id)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": file_url
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
def DownloadRecord_delete(request):  # 删除下载记录
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'POST':
            user_id = jwt_code['user_id']
            file_id = request.POST.get('file_id')
            relation_obj = DownloadFile_post.objects.filter(userID=user_id, fileID=file_id)
            relation_obj.delete()
            file_num = dashboard.objects.filter(user_id=user_id).values('DownloadFile_num')[0]['DownloadFile_num']
            if file_num == 0:
                file_num = 1
            file_num = file_num-1
            dashboard.objects.filter(user_id=user_id).update(DownloadFile_num=file_num)
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": True
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
def search_file(request):
    jwt_code = jwt_auth.jwt_sys(request).main()
    if jwt_code['is_real']:
        if request.method == 'GET':
            file_list_id = []
            search_content = request.GET.get('search_content')
            # 优先全字段匹配
            bestfiles_id = file.objects.filter(name__icontains=search_content).values_list('id',flat=True)
            file_list_id.extend(bestfiles_id)
            # 字段拆分匹配
            word_list = jieba.cut(search_content, cut_all=True)
            for word in word_list:
                suggestfiles_id = file.objects.filter(name__icontains=word).values_list('id',flat=True)
                file_list_id.extend(suggestfiles_id)
            file_list_id = list(set(file_list_id))  # 搜索去重
            file_list = []
            for i in file_list_id:
                file_list.extend(file.objects.filter(id=i).values('id', 'auth_id', 'name', 'suffix', 'address', 'size', 'department', 'subject', 'readme', 'download_num', 'auth_name'))
            response = {
                "code": "00000",
                "msg": "请求成功",
                "data": file_list
            }
            return JsonResponse(response)
        else:
            debug_msg = "request.method=" + str(request.method)
            response = {
                "code": "A0400",
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