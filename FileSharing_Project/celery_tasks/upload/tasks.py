from Files.osssys import Oss
from celery_tasks.main import celery_app


@celery_app.task(name='UploadFile')
def UploadFile(file_name, fileobj):
    is_update = Oss().upload_file(filename=file_name, file=fileobj.read())
    if is_update is False:
        raise PermissionError('上传失败')
