import jwt
import datetime
import time

class jwt_sys():
    def __init__(self,req):
        self.req = req

    def create_jwt(self,user_id):
        tm = time.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
        out_time = datetime.datetime.now()+datetime.timedelta(days=1)
        tm_e = time.strptime(out_time.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
        dic = {
            'exp': time.mktime(tm_e),
            'iat': time.mktime(tm),
            'iss': 'ziqiang',
            'data': user_id,
        }
        s = jwt.encode(dic,'secret',algorithm='HS256')
        return s

    def get_jwt(self):
        token = self.req.META.get('HTTP_AUTHORIZATION')
        return token

    def parse_jwt(self,token):
        s = jwt.decode(token,'secret',issuer='ziqiang',algorithms=['HS256'])
        return s

    def is_out_time(self,s):
        tm = time.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
        datetime_now = time.mktime(tm)
        end_time = s['exp']
        if datetime_now < end_time:
            return True
        else:
            return False

    def get_user_id(self,token):
        user_id = jwt.decode(token, 'secret', issuer='ziqiang', algorithms=['HS256'])['data']
        return user_id

    def main(self):
        token = self.get_jwt()
        if token is not None and token != '':
            s = self.parse_jwt(token)
            if self.is_out_time(s) is True:
                user_id = self.get_user_id(token)
                return {'is_real':True,'user_id':user_id}
            else:
                return {'is_real': False}
        else:
            return {'is_real': False}