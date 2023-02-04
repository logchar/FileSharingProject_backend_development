import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Users.models import User, Dashboard
from FileSharing_Project.jwt_auth import jwt_sys


@csrf_exempt
def log_reg(request):
    wxcode = request.POST.get('code')
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": "wx984d508ce8f82e87",
        "secret": "eef65ed22dda055a3e62ffd47ec260c8",
        "js_code": wxcode,
        "grant_type": "authorization_code",
    }
    res = requests.get(url=url, params=params)
    openid = res.json()['openid']
    if User.objects.filter(openid=openid).exists():
        user_obj = User.objects.get(openid=openid)
    else:
        nickname = "用户_" + str(User.objects.all().count()+1)
        user_obj = User.objects.create(openid=openid, nickname=nickname)
        dashboard_obj = Dashboard(user=user_obj, collection_num=0, UploadFile_num=0, DownloadFile_num=0)
        dashboard_obj.save()
    token = jwt_sys(request).create_jwt(user_obj.id)
    response = {
        "code": "00000",
        "msg": "请求成功",
        'token': token,
    }
    return JsonResponse(response)
