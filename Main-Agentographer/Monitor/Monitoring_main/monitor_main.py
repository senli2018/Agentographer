import time
import requests
import cv2
from PIL import Image
import csv
import threading
import time
import requests
import json
from tem_matching_input import match_template
import os
import datetime
from llma import upload_file,call_llama_api


def get_picture_computer_HDMI():

    start_time = datetime.datetime.now()
    print("cap开始时间:", start_time)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
    end_time = datetime.datetime.now()
    print("cap结束时间:", end_time)
    elapsed_time = end_time - start_time
    print("cap运行时间:", elapsed_time)
    if not cap.isOpened():
        print("无法打开视频采集卡")
        return None, None
    # 设置分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # 设置宽度
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # 设置高度
    # 读取第一帧视频
    start_time = datetime.datetime.now()
    print("ret, frame开始时间:", start_time)
    # 等待相机初始化
    time.sleep(2)  # 增加延迟，等待相机准备好
    # 丢弃前几帧
    for _ in range(5):
        cap.read()
    ret, frame = cap.read()
    end_time = datetime.datetime.now()
    print("ret, frame结束时间:", end_time)
    elapsed_time = end_time - start_time
    print("ret, frame运行时间:", elapsed_time)
    if not ret:
        print("无法接收视频帧（可能是视频流结束或者错误）")
        cap.release()
        return None, None
    # 保存图片并设置JPEG质量
    image_path = 'voice_new/captured_image_computer.jpg'
    cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])








# 第一部分：判断姿势是否标准
def check_pose():
    global pose  # 使用全局变量存储姿势的判定
    with open(r"D:\Monitoring_AI\txt\if_move_bed.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
        text = lines[0].strip()  # 读取第一行并去除可能的空白字符
    if int(text) == 0:
        url = 'http://192.168.1.195:5000/api/gptpicture/' # 2080做判断返回结果
        response = requests.get(url)
        print(f'判断姿势的：接口传过来的数据：{response.text}')
        data_picture = json.loads(response.text)
        print(f"判断姿势的：解码之后的数据:", data_picture)
        data_picture = json.loads(data_picture)
        assignment_results = {}
        for key, value in data_picture.items():
            if value == "是":
                assignment_results[key] = 1
            else:
                assignment_results[key] = 0
        data_picture1 = assignment_results["1"]
        data_picture2 = assignment_results["2"]
        pose = 1 if (data_picture1 == 1 and data_picture2 == 1) else 0
        file=r'D:\Monitoring_AI\txt\if_pose_right.txt'
        with open(file, 'w', encoding='utf-8') as file:
            file.write(str(pose))
            file.flush()
    else:
        pose = 1
        print("手动赋值姿势为：", pose)

# 第二部分：判断门是否开着以及屋内人数
def check_door_and_people():
    global data_video1, data_video2  # 使用全局变量存储大门和人数的信息
    url = 'http://192.168.1.195:5000/api/gptvideo/' # 人数由2080做判断返回结果
    response = requests.get(url)
    print(f"判断大门和人数的数据: {response.text}")
    data_video = json.loads(response.text)

    url = 'http://192.168.1.195:5000/api/gptdoor/'  # 大门由2080做判断返回结果
    response = requests.get(url)
    data_video1 = int(json.loads(response.text)) # 1代表大门是开的，0代表大门是关闭的
    data_video2 = int(data_video)  # 0代表没有人，1代表有一个人，2代表有多个人。

def check_pose_post():
    url = 'http://192.168.1.195:5000/api/gptpost/' # 人数由2080做判断返回结果
    response = requests.get(url)
    print(f"判断患者是否躺在托里的数据: {response.text}")
    data_video = json.loads(response.text)
# 第三部分：采集卡和模板匹配
def template_matching():
    global data_cv  # 使用全局变量存储模板匹配的结果
    while True:
        with open(r"D:\Monitoring_AI\txt\Obs_if_use.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()
            text = lines[0].strip()  # 读取第一行并去除可能的空白字符
        if int(text) == 0:
            with open(r"D:\Monitoring_AI\txt\Obs_if_use.txt", 'w', encoding='utf-8') as file:
                file.write(f"1\n")
            break
        else:
            print("等待0.5s，其他设备使用完毕")
            time.sleep(0.5)

    get_picture_computer_HDMI()
    with open(r"D:\Monitoring_AI\txt\Obs_if_use.txt", 'w', encoding='utf-8') as file:
        file.write(f"0\n")

    input_image_path = r"voice_new\captured_image_computer.jpg"
    data_cv = match_template(input_image_path)

# 主函数：初始化并启动所有线程
def monitor():
    # 定义线程
    pose_thread = threading.Thread(target=check_pose)  #  得到pose状态
    door_and_people_thread = threading.Thread(target=check_door_and_people) # 得到data_video1大门状态 data_video2人数状态
    template_matching_thread = threading.Thread(target=template_matching) # 得到联影屏幕状态

    # 启动线程
    pose_thread.start()
    door_and_people_thread.start()
    template_matching_thread.start()

    # 等待所有线程执行完毕
    pose_thread.join()
    door_and_people_thread.join()
    template_matching_thread.join()

    # 返回最终结果
    return int(data_video1), int(data_video2), pose, data_cv



def load_state_mapping(filename):
    """从文件中加载状态映射表"""
    state_mapping = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (
            int(row[' Door_State']), int(row[' People_Count']), int(row[' Posture_State']), int(row[' Interface_State']))
            state_mapping[key] = row[' State']
    return state_mapping


def get_state_description(input_tuple):
    """根据输入的状态组合返回对应的状态描述
    """
    # 加载状态映射表
    state_mapping = load_state_mapping(r"logical_document_use.txt")
    return state_mapping.get(input_tuple, "Status not found")


def monitor_analyzing():

    data = monitor()                                           # 获取四个状态信息
    result = get_state_description(data)
    print(result)

    # 检查文件是否存在，如果不存在则创建文件
    file_path = r"D:\Monitoring_AI\txt\processtest.txt"
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            # 文件不存在时，这里可以执行一些初始化操作，例如写入文件头信息等
            pass  # 如果不需要初始化操作，可以保留这一行为空
    # 将变量写入到txt文件中
    with open(file_path, 'w', encoding='utf-8') as file:
            file.write(result)                                  # 将匹配到的status写入文件
            file.flush()

    return result

if __name__ == '__main__':
    while True:
        monitor_analyzing()
        time.sleep(2)
    # get_picture_computer_HDMI()
    # 监控分析()
    # check_pose_post()























