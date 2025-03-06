import time
from openai import OpenAI

'''
@Project : Agent_lab 
@File    : upload_file.py
@IDE     : PyCharm 
@Author  : Kyson. Li
@Date    : 2024/1/15 19:10 
'''
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys

def upload_file(local_file_path):
    # 替换为用户的 secretId
    secret_id = 'AKIDMbgePvJnCZn076tTYXO930ru0uso6WZh'
    # 替换为用户的 secretKey
    secret_key = 'NXTBj6II5kEZH0c7PYaqEUvX2Qq8IJYj'
    # 替换为用户的 Region
    region = 'ap-beijing'
    # 替换为用户的 bucket
    bucket = 'paper86ye-1317959654'

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    # 生成 cos 客户端。
    client = CosS3Client(config)

    # 上传文件
    response = client.upload_file(
        Bucket=bucket,
        LocalFilePath=local_file_path,
        Key=local_file_path,
    )

    # 返回公开访问的文件URL
    public_url = f"https://{bucket}.cos.{region}.myqcloud.com/{local_file_path[2:]}"
    print(public_url)

    return public_url

def analyze_img(prompt="这张图片是一个患者在CT方舱中做CT检查过程中拍摄的，请问患者在检查CT的过程中最可能是在什么进度",img_path="https://bj-1323287448.cos.ap-beijing.myqcloud.com/stand_test.png"):
    client = OpenAI(
        # #将这里换成你在aihubmix api keys拿到的密钥
        api_key="sk-z8Keo9iBzrPPkWTVKy7IHtSmvm0BWlLnyaNeVonaludm3pzW",
        # 这里将官方的接口访问地址，替换成aihubmix的入口地址
        base_url="https://api.mobrai.cc/v1"
    )

    response = client.chat.completions.create(
        #model="gpt-4-vision-preview",
        model="gpt-4o",

        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_path,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    s_time=time.time()
    result=analyze_img()
    print(result)
    e_time=time.time()
    print(e_time-s_time)