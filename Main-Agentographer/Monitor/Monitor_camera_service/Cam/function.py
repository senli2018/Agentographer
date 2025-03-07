import cv2
import requests
import json
import time
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
def common_cam():
    # 打开摄像头（0表示第一个摄像头）

    try:
        cap = cv2.VideoCapture(2)
        # 检查摄像头是否成功打开
        if not cap.isOpened():
            print("无法打开摄像头")
            exit()
        # 读取一帧图像
        ret, frame = cap.read()
        # 检查是否成功读取帧
        if not ret:
            print("无法接收帧（可能是摄像头问题）")
            exit()
        # 保存图像到本地路径
        file_name = r'/home/senlee/data1/joe/Guoaoshuai/small_computer_copy/Cam/picture_tmp/captured_image.jpg'
        cv2.imwrite(file_name, frame)
        # 释放摄像头
        cap.release()
        # 销毁所有窗口
        cv2.destroyAllWindows()
        print("图像已保存到", file_name)
    except Exception as e:
        print(f"error:{e}")
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()

LLAMA_API_URL = "https://a900-36-139-230-162.ngrok-free.app/v1/chat/completions"  # 替换为你的API地址

def upload_file(local_file_path):
    # 替换为用户的 secretId
    secret_id = ''
    # 替换为用户的 secretKey
    secret_key = ''
    # 替换为用户的 Region
    region = 'ap-beijing'
    # 替换为用户的 bucket
    bucket = ''
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

def call_llama_api(messages, image_path, max_retries=3, retry_delay=5):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    for attempt in range(max_retries):
        try:
            # 构建请求数据
            payload = {
                "model": "llama-2-13b-chat",
                "messages": [],
                "stream": False,
                "max_tokens": 1024,
                "temperature": 0.7
            }

            # 处理消息和图片
            for msg in messages:
                if msg.get("content"):
                    if msg.get("role") == "user" and "<image>" in msg["content"]:
                        payload["messages"].append({
                            "role": msg.get("role", "user"),
                            "content": [
                                {
                                    "type": "text",
                                    "text": msg["content"].replace("<image>", "").strip()
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_path
                                    }
                                }
                            ]
                        })
                    else:
                        payload["messages"].append({
                            "role": msg.get("role", "user"),
                            "content": msg["content"].strip()
                        })

            # 打印请求信息（调试用）
            print(f"\n发送请求到: {LLAMA_API_URL}")
            print(f"请求数据: {json.dumps(payload, ensure_ascii=False, indent=2)}")
            # 发送请求
            response = requests.post(LLAMA_API_URL, json=payload, headers=headers, timeout=30)
            # 检查响应状态
            if response.status_code != 200:
                print(f"API响应错误 - 状态码: {response.status_code}")
                print(f"错误详情: {response.text}")
                if attempt < max_retries - 1:
                    print(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    continue
                return None
            # 解析响应数据
            response_data = response.json()
            if not response_data.get("choices"):
                print("API响应格式错误: 未找到'choices'字段")
                return None
            return response_data['choices'][0]['message']['content']
        except FileNotFoundError as e:
            print(f"文件错误: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {str(e)}")
            print(f"原始响应: {response.text}")
            if attempt < max_retries - 1:
                print(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                continue
            return None
        except requests.RequestException as e:
            print(f"请求错误: {str(e)}")
            if attempt < max_retries - 1:
                print(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                continue
            return None
        except Exception as e:
            print(f"未知错误: {str(e)}")
            return None
    return None


def zhipu_mmodel_picture(image_data):
    import base64
    from zhipuai import ZhipuAI
    import datetime
    # 输出开始时间
    start_time = datetime.datetime.now()
    img_paths = [
        image_data,
    ]
    # 将每张图片转换为Base64编码
    images_base64 = []
    for img_path in img_paths:
        with open(img_path, 'rb') as img_file:
            img_base = base64.b64encode(img_file.read()).decode('utf-8')
            images_base64.append({
                "type": "image_url",
                "image_url": {
                    "url": img_base
                }
            })

    # 创建包含所有图片和文本的content数组
    content = [
        {
            "role": "user",
            "content": images_base64 + [
                {
                    "type": "text",
                    "text":
                        """
                        你看到的是一张CT间的图，现在请你只使用"是"、"否"两个答案，严格按照顺序回答如下2个问题：1、患者平躺在床上？2、患者的胳膊向CT机器方向上举？,请用json的格式。
                        严格用以下格式来：例如
                        {
                            "1": "否",
                            "2": "否"
                        }
                        """
                    # 6. 扫描床的状态：如果图片展示的过程是扫描床在最低点保持不动，请回答“扫描床在最底部”；如果图片展示的过程是床在升高，请回答“扫描床在升床”；如果图片展示的过程是床在下降，请回答“扫描床在降床”；如果图片展示的过程是床向右移动，请回答“扫描床在进床”；如果床向左移动，请回答“扫描床在退床”。
                }
            ]
        }
    ]

    # 初始化ZhipuAI客户端
    client = ZhipuAI(api_key="")  # 填写您自己的APIKey

    # 发送请求
    response = client.chat.completions.create(
        model="glm-4v-plus",  # 填写需要调用的模型名称
        messages=content,
        temperature=0.01,  # 设置温度参数为0.5
        top_p=0.9  # 设置核采样参数为0.9
    )

    # 打印响应消息
    print(response.choices[0].message.content)
    # 输出结束时间
    end_time = datetime.datetime.now()
    # print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return response.choices[0].message.content


def zhipu_model_video(image_data):
    import base64
    from zhipuai import ZhipuAI
    import datetime
    # 输出开始时间
    start_time = datetime.datetime.now()
    # print("程序开始时间:", start_time)
    # # 假设我们有多个图片路径
    # img_paths = [
    #     "./video_ct/标准2.jpg",
    # ]
    img_paths = [
        image_data,
    ]
    # 将每张图片转换为Base64编码
    images_base64 = []
    for img_path in img_paths:
        with open(img_path, 'rb') as img_file:
            img_base = base64.b64encode(img_file.read()).decode('utf-8')
            images_base64.append({
                "type": "image_url",
                "image_url": {
                    "url": img_base
                }
            })

    # 创建包含所有图片和文本的content数组
    content = [
        {
            "role": "user",
            "content": images_base64 + [
                {
                    "type": "text",
                    "text":
                        """
                        根据图片判断屋内的人数。不要将电视机上的人物计入屋内人数。请根据以下规则回答：
                            如果屋内没有人，回答“0”；
                            如果屋内有一个人，回答“1”；
                            如果屋内有多个人，回答“2”。
                        请严格按照以上规则回答。
                        """

                }

            ]
        }
    ]

    # 初始化ZhipuAI客户端
    client = ZhipuAI(api_key="")  # 填写您自己的APIKey

    # 发送请求
    response = client.chat.completions.create(
        model="glm-4v-plus",  # 填写需要调用的模型名称
        messages=content,
        temperature=0.01,  # 设置温度参数为0.5
        top_p=0.9  # 设置核采样参数为0.9
    )

    # 打印响应消息
    print(response.choices[0].message.content)
    # 输出结束时间
    end_time = datetime.datetime.now()
    # print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return response.choices[0].message.content


def Big_model_picture():
    # pose   deep
    output_file = r"/home/senlee/data1/joe/Guoaoshuai/small_computer_copy/Cam/picture_tmp/captured_image_clothes.jpg"
    image_path = upload_file(output_file)
    message1 = [
        {"role": "user",
         "content": "大门是开的还是关闭的，请用0和1来回复，1代表开着，0代表关着"}
    ]
    data = call_llama_api(message1, image_path)
    return data


def Big_model_video():
    # person number
    output_file = r"/home/senlee/data1/joe/Guoaoshuai/small_computer_copy/Cam/picture_tmp/captured_image_clothes.jpg"
    image_path = upload_file(output_file)
    message2 = [
        {"role": "user",
         "content": """
                    根据图片判断屋内的人数。不要将电视机上的人物计入屋内人数。请根据以下规则回答：
                    如果屋内没有人，回答“0”；
                    如果屋内有一个人，回答“1”；
                    如果屋内有多个人，回答“2”。
                    请严格按照以上规则回答。
                    """
         }
    ]
    data = call_llama_api(message2, image_path)
    return data


def if_open_door():
    # door
    output_file = r"/home/senlee/data1/joe/Guoaoshuai/small_computer_copy/Cam/picture_tmp/captured_image_clothes.jpg"
    image_path = upload_file(output_file)
    message3 = [
        {"role": "user",
         "content":
             """
             你看到的是一张CT间的图，现在请你只使用"是"、"否"两个答案，严格按照顺序回答如下2个问题：1、患者平躺在床上？2、患者的胳膊向CT机器方向上举？,请用json的格式。
             严格用以下格式来：例如
             {
                 "1": "否",
                 "2": "否"
             }
             """
         }
    ]
    data = call_llama_api(message3, image_path)
    return data


if __name__ == '__main__':
    Big_model_picture()     # pose if ok
    Big_model_video()       # people count
    if_open_door()          # clothes

