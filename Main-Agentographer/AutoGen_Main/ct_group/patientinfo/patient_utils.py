import cv2
from PIL import Image
import json
from PIL import Image, ImageEnhance
from CFG_GLOBAL import AGENT_RUN_DIR
import os
def enhance_image(input_path, output_path):
    image = Image.open(input_path)

    enhancer = ImageEnhance.Sharpness(image)
    image_enhanced = enhancer.enhance(2.0)
    contrast_enhancer = ImageEnhance.Contrast(image_enhanced)
    image_final = contrast_enhancer.enhance(1.5)

    image_final.save(output_path)
def get_picture_ocr():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("The video capture card cannot be opened.")
        return None, None

    # 设置分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)  # 设置宽度
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)  # 设置高度
    # 读取第一帧视频
    ret, frame = cap.read()

    if not ret:
        print("Unable to receive video frames (possibly due to the end of the video stream or an error)")
        cap.release()
        return None, None

    # 保存图片并设置JPEG质量
    image_path = '.\img_temp\captured_image_ocr.jpg'

    cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print(f"The picture is saved as {image_path}")
    # 调用增强图像函数
    enhance_image(image_path, image_path)
    # 转换为PIL图像对象
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)
    # image.show()
    # 释放资源
    cap.release()
    return image

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

def ocr(public_url):
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key="fecf27dd25b5000a15a97279d0363e3c.TtcevCAzNj8IYtIR")  # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4v",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": public_url
                        }
                    },
                    {
                        "type": "text",
                        "text": "请识别出来以下信息1、只识别（病人的ID）后面的字母和数字，不能包含ID两个字母：。2、姓名：。3、性别：。4、检查项目：。5、出生日期：(只识别年份数字)。"
                                "请以如下格式返回：{\"ID\": \"...\", \"Name\": \"...\", \"Gender\": \"...\", \"Examination\": \"...\", \"年龄\": \"...\"}"
                    }
                ]
            }
        ]

    )
    result=response.choices[0].message.content
    result=result.replace("```json\n\n", "")
    result=result.replace("\n\n```", "")
    print(result)
    return result

#保存成文件
def result_save(data):
    data = json.loads(data)
    print(data)
    # 将字典转换为字符串
    data_str = json.dumps(data, ensure_ascii=False)
    # 写入文件
    with open('data.txt', 'a', encoding='utf-8') as file:
        file.write(data_str + '\n')

def OcrRecognize():
    get_picture_ocr()
    image_path= "./img_temp/captured_image_ocr.jpg"
    # image_path = "D:\\AgentAI\\img_temp\\captured_image_ocr.jpg"
    public_url = upload_file(image_path)
    result=ocr(public_url)
    result_save(result)
    return "病人信息已保存到data.txt"

def read_first_line():
    with open("data.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 获取第一行内容
    first_line = lines[0].strip()
    print(first_line)
    # 删除第一行
    with open("data.txt", 'w', encoding='utf-8') as file:
        file.writelines(lines[1:])

    # 写入新文件
    with open("data_finsh.txt", 'a', encoding='utf-8') as new_file:
        new_file.write(first_line + '\n')

    #TODO 为了记录数据
    with open(r"txt/process_time.txt", 'a', encoding='utf-8') as new_file:
        new_file.write(first_line + '\n')

    return first_line


import re

# 读取文件内容
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# 解析文件内容并创建字典
def parse_to_dict(lines):
    actions_dict = {}
    for line in lines:
        match = re.match(r'(\d{2}点\d{2}分\d{2}秒):action\[(.+?)\]', line)
        if match:
            timestamp = match.group(1)
            action = match.group(2)
            actions_dict[timestamp] = f'action[{action}]'
    return actions_dict

# 将字典写入新的TXT文件
def write_dict_to_file(dict_data, file_path):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write('{\n')
        for i, (timestamp, action) in enumerate(dict_data.items()):
            file.write(f'  {timestamp}:{action}；\n')
            if i < len(dict_data) - 1:
                file.write('  ')
        file.write('}\n')

# 主函数
def save_dict():
    input_file_path = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    output_file_path = os.path.join(AGENT_RUN_DIR,'txt/process_time.txt')
    lines = read_file(input_file_path)
    actions_dict = parse_to_dict(lines)
    write_dict_to_file(actions_dict, output_file_path)
    print(f'Dictionary has been written to {output_file_path}')
if __name__ == '__main__':
    data= read_first_line()
    data = json.loads(data)
    id=data["ID"]
    print(id)

