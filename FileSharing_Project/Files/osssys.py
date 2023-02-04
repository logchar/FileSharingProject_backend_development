import oss2


class Oss:

    def __init__(self):
        self.accessKeyId = "LTAI5tAu8fZpvMspEemMjr9c"
        self.accessKeySecret = "9u0iSlEB9EyldZlVppekC9ru8LJ1JT"
        self.endpoint = "oss-cn-hangzhou.aliyuncs.com"
        self.bucketName = "ziqiang-resource"

    def upload_file(self, filename, file):
        auth = oss2.Auth(self.accessKeyId, self.accessKeySecret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucketName, connect_timeout=60)
        res = bucket.put_object(filename, file)
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
