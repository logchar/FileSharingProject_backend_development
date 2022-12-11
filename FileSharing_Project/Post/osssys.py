import oss2


class Oss:

    def __init__(self):
        self.accessKeyId = "LTAI5t9ex2r4GWHcu3tHZwPU"
        self.accessKeySecret = "laBUFWj3Aj1ZU0uw5rZsK13RxwjYgN"
        self.endpoint = "oss-cn-hangzhou.aliyuncs.com"
        self.bucketName = "zq-rookie-file-sharing"

    def upload_file(self, file, auth_id, name, file_id, suffix):
        file_name = str(auth_id)+"_"+name+"_"+str(file_id)+"."+suffix  # 用户id_文件名_文件id.后缀
        auth = oss2.Auth(self.accessKeyId, self.accessKeySecret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucketName, connect_timeout=60)
        res = bucket.put_object(file_name, file)
        if res.status // 100 == 2:
            return True
        else:
            return False

    def delete_file(self, name):
        auth = oss2.Auth(self.accessKeyId, self.accessKeySecret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucketName, connect_timeout=60)
        res = bucket.delete_object(name)
        if res.status // 100 == 2:
            return True
        else:
            return False

    def get_url(self, file_name):
        return "https://"+self.bucketName + "." + self.endpoint + "/" + file_name

    def get_suffix(self, url):
        suffix = url.split('.')[-1]
        return suffix
