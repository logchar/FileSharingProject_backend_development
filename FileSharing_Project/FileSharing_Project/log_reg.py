import urllib
import json
import time
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from User.models import user, dashboard
from FileSharing_Project.jwt_auth import jwt_sys

@csrf_exempt
def log_reg(request):

    if request.method == 'POST':
        wxcode = request.POST.get('code')
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {"appid": "wx984d508ce8f82e87", "secret": "eef65ed22dda055a3e62ffd47ec260c8", "js_code": wxcode, "grant_type": "authorization_code"}
        res = requests.get(url=url, params=params)
        res_dic = json.loads(res.json())
        openid = res_dic['openid']
        if user.objects.filter(openid=openid).exists():
            user_id = user.objects.filter(openid=openid).values('id')[0]['id']
        else:
            nickname = "用户_" + str(openid)
            user_obj = user.objects.create(openid=openid,nickname=nickname)
            user_id = user_obj.id
            user_obj = user.objects.get(id = user_id)
            dashboard_obj = dashboard(user=user_obj,collection_num=0,UploadFile_num=0,DownloadFile_num=0)
            dashboard_obj.save()
        token = jwt_sys(request).create_jwt(user_id)
        response={
            "code":"00000",
            "msg":"请求成功",
            "data":{
                'token':token,
                'user_id':user_id
            }
        }
        return JsonResponse(response)
    else:
        debug_msg="request.method="+str(request.method)
        response={
            "code":"",
            "msg":"请求失败，方法错误",
            "debug":debug_msg,
            "data":False
        }
        return JsonResponse(response)