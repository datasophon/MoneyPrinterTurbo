# -*- coding:utf-8 _*_
"""
@Project    : MQJCTools
@File       : minio_utils.py
@Author     : 晴羽
@CreateTime : 2024-05-22 10:20
"""
import os
import mimetypes
from loguru import logger
from datetime import timedelta, datetime
from minio import Minio, S3Error

MINIO_HOST = 'objectstorageapi.bja.sealos.run'
MINIO_ACCESS_KEY = '7jjsgq26'
MINIO_SECRET_KEY = 'mlls5knrw5kwm4jp'
client = Minio(
        endpoint=MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=True)



def upload_local_file(bucket_name: str, local_file_path: str, object_name: str):
    """
    上传本地文件对象
    :param bucket_name: 存储桶名
    :param local_file_path: 本地文件路径
    :param object_name: 桶对象名
    :return: 返回对象访问地址
    """
    # 获取文件类型
    content_type, _ = mimetypes.guess_type(local_file_path)
    # 获取文件后缀
    _, file_extension = os.path.splitext(local_file_path)
    logger.info(f'本地开始上传文件 文件类型: {content_type}')
    client.fput_object(bucket_name=bucket_name, object_name=object_name, file_path=local_file_path,
                            content_type=content_type if content_type else 'application/octet-stream')
    logger.info('本地文件上传完成')
    object_url = client.get_presigned_url('GET', bucket_name, object_name)
    object_url = remove_after_question_mark(object_url)
    logger.info(f'对象访问地址: {object_url}')
    return object_url

def remove_after_question_mark(s):
    index = s.find('?')
    if index != -1:
        return s[:index]
    else:
        return s  # 如果没有找到问号，则返回原始字符串



if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)

    bucket_names = '7jjsgq26-simon'
    local_file = f'D:\\text2video\MoneyPrinterTurbo\storage\\tasks\\4c1c8153-7c9a-4bb2-a575-5853d3380ae8\\final-1.mp4'

    url = 'https://pic.netbian.com/uploads/allimg/240322/233416-1711121656e5bd.jpg'

    # 上传本地资源
    video_url = upload_local_file(bucket_names,local_file,'test')
    print(video_url)



    # 上传远程资源
    # minio_client.upload_remote_file(bucket_name=bucket_names, remote_addr=url, object_name=filename)
    # print(minio_client.get_bucket_object_url(bucket_name=bucket_names))

