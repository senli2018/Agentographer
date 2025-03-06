import cv2
import numpy as np
from PIL import Image
# 打开视频采集卡设备，假设设备索引为0
import datetime
import time
import re
from tem_img_seg import ocr_crop_input_inbed_screen,ocr_crop_scout



def get_picture_computer_HDMI():

    start_time = datetime.datetime.now()
    print("cap开始时间:", start_time)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
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
    image_path = 'D://AgentAI_ls_309//voice_new//captured_image_computer.jpg'
    cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

def read_golbol_var():

    # 读取文件内容
    with open(r"D:\Monitoring_AI\txt\golbal.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 检查文件是否至少有一行
    if len(lines) > 0:
        # 取出第一行
        first_line = lines[0]
        print(first_line)
        # # 覆盖写入数字0
        # with open(r"D:\AgentAI_ls\golbal.txt", 'w', encoding='utf-8') as file:
        #     file.write('0\n')  #
    return first_line
def get_value(input_str):
    match = re.search(r":\s*(\d+)", input_str)
    if match:
        value = int(match.group(1))
        print(value)  # 输出: 1
        return value

def template_matching_two(input_image_path, match_status):
    template_paths = [
        r"after_seg\2-1.jpg",
        r"after_seg\2-2.jpg",
    ]
    # 读取输入图像
    input_img = cv2.imread(input_image_path, cv2.IMREAD_COLOR)

    # 遍历每一个模板图像
    for i, template_path in enumerate(template_paths):
        # 读取模板
        template_img = cv2.imread(template_path, cv2.IMREAD_COLOR)

        # 使用模板匹配
        result = cv2.matchTemplate(input_img, template_img, cv2.TM_CCOEFF_NORMED)

        # 设置匹配阈值
        threshold = 0.8

        # 找到匹配的位置
        loc = np.where(result >= threshold)

        # 如果找到匹配
        if len(loc[0]) > 0:
            print(f"Match found for template: {template_path}")

            if i == 0:
                match_status['输入进床深度和下界的界面'] = 2
                print("现在输入进床深度和下界的界面")
                return "现在输入进床深度和下界的界面"
            elif i == 1:
                match_status['定位片界面'] = 3
                print("现在定位片界面")
                return "现在定位片界面"

    print("No match found in template_matching_two.")
    return "No match found"

def template_matching_three(input_image_path, match_status):
    template_paths = [
        r"after_seg\3-2.jpg",
        r"after_seg\3-3.jpg",
    ]
    # 读取输入图像
    input_img = cv2.imread(input_image_path, cv2.IMREAD_COLOR)

    # 遍历每一个模板图像
    for i, template_path in enumerate(template_paths):
        # 读取模板
        template_img = cv2.imread(template_path, cv2.IMREAD_COLOR)

        # 使用模板匹配
        result = cv2.matchTemplate(input_img, template_img, cv2.TM_CCOEFF_NORMED)

        # 设置匹配阈值
        threshold = 0.8

        # 找到匹配的位置
        loc = np.where(result >= threshold)

        # 如果找到匹配
        if len(loc[0]) > 0:
            print(f"Match found for template: {template_path}")

            if i == 0:
                match_status['正片扫描界面'] = 5
                print("现在正片扫描界面")
                return "现在正片扫描界面"
            elif i == 1:
                match_status['退床界面'] = 6
                print("现在退床界面")
                return "现在退床界面"

    print("No match found in template_matching_three.")
    return "No match found"



#TODO 这个是和每个模板进行匹配，寻找相似度最大的然后进入逻辑
def match_template(input_image_path):
    match_status = {
        '患者信息输入界面': 0,
        '输入进床深度和下界的界面': 0,
        '定位片界面': 0,
        '调整定位片范围界面': 0,
        '正片扫描界面': 0,
        '退床界面': 0
    }

    template_paths = [
        r"after_seg\1.jpg",
        r"after_seg\2.jpg",
        r"after_seg\3.jpg",
        r"after_seg\4.jpg",
        r"after_seg\5.jpg"
    ]

    # 读取输入图像
    input_img = cv2.imread(input_image_path, cv2.IMREAD_COLOR)

    # 初始化最高相似度和对应的模板索引
    max_similarity = 0
    best_match_index = -1

    # 遍历每一个模板图像
    for i, template_path in enumerate(template_paths):
        # 读取模板
        template_img = cv2.imread(template_path, cv2.IMREAD_COLOR)

        # 使用模板匹配
        result = cv2.matchTemplate(input_img, template_img, cv2.TM_CCOEFF_NORMED)

        # 找到最大相似度
        min_val, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val > max_similarity:
            max_similarity = max_val
            best_match_index = i

    # 如果找到匹配
    if best_match_index != -1:
        print(f"Best match found for template: {template_paths[best_match_index]}")

        # 根据最佳匹配的模板索引执行相应的子逻辑
        if best_match_index == 0:
            match_status['患者信息输入界面'] = 1
            print("现在是患者信息输入界面")
        elif best_match_index == 1:
            print("现在输入进床深度和下界的界面")
            output_image_path = ocr_crop_input_inbed_screen(input_image_path)
            template_matching_two(output_image_path, match_status)
        elif best_match_index == 2:
            first_line = read_golbol_var()
            if int(first_line) == 0:
                print("0")
                match_status['调整定位片范围界面'] = 4
                print("现在调整定位片范围界面")
            else:
                print("1")
                output_image_path = ocr_crop_scout(input_image_path)
                template_matching_three(output_image_path, match_status)
        elif best_match_index == 3:
            match_status['退床界面'] = 6
            print("现在是退床界面")
        elif best_match_index == 4:
            first_line = read_golbol_var()
            if int(first_line) == 0:
                print("0")
                match_status['调整定位片范围界面'] = 4
                print("现在调整定位片范围界面")
            else:
                print("1")
                output_image_path = ocr_crop_scout(input_image_path)
                template_matching_three(output_image_path, match_status)

    # 打印并返回匹配状态
    filtered_data = {key: value for key, value in match_status.items() if value != 0}
    print(filtered_data)
    filtered_data = str(filtered_data)
    filtered_data = get_value(filtered_data)
    return filtered_data
if __name__ == "__main__":
    get_picture_computer_HDMI()



