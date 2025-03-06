import time
import cv2
from pose_request.position_request import ct_seg_request
from ct_group.mk_control.mk_utils import pull_locator_fixed, pull_locator_fixed_left, pull_locator_fixed_right, \
        pull_locator_fixed_middle
from ct_group.visionAi.vision_utils import get_picture_computer_HDMI
import json
import time
from ct_group.mk_control.mk_utils import KeyPress
from ct_group.ct_control.ct_utils import pcb_up
from pose_request.position_request import deep_camera
from PIL import Image
# 打开视频采集卡设备，假设设备索引为0
import datetime
import json
import requests
from ct_group.ct_control.ct_utils import pcb_quit_bed
from ct_group.ct_control.ct_utils import button_close_all_system_check
from ct_group.mk_control.mk_utils import input_patient_id
import traceback

def get_picture_computer_HDMI():
    # 打开视频采集卡设备，假设设备索引为0
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("无法打开视频采集卡")
        return None, None

    # 设置分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)  # 设置宽度
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # 设置高度
    desire_height = 1080
    desire_width = 1920//2
    import time
    # 等待相机初始化
    time.sleep(2)  # 增加延迟，等待相机准备好
    # 丢弃前几帧
    for _ in range(5):
        cap.read()
    # 读取第一帧视频
    ret, frame = cap.read()
    # frame = cv2.resize(frame, [desire_height, desire_width])
    frame = cv2.resize(frame, [desire_width, desire_height])
    # print(frame.shape)
    if not ret:
        print("无法接收视频帧（可能是视频流结束或者错误）")
        cap.release()
        return None, None

    # 保存图片并设置JPEG质量
    # image_path = 'D://AgentAI_ls//iner_pic//captured_image_computer.jpg'
    # cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    #构造新的文件路径
    image_path = f'/iner_pic/captured_image_computer.jpg'
    cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print(f"图片已保存为 {image_path}")
    # 转换为PIL图像对象
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)
    # 释放资源
    cap.release()
    return image
def adjust_range_scan():
    """调整定位片范围
    """
    data = get_picture_computer_HDMI()
    # 分部分割算法获取肺部的上下范围，并进行一定固定值加减
    result_data = ct_seg_request(data)
    # print(f"Received data: {result_data}")
    result_dict = json.loads(result_data)
    up_bound = result_dict['top_pos']
    up_bound = int(up_bound) - 40
    up_bound = int(up_bound)
    # print("调整完肺部的上界", up_bound)
    down_bound = result_dict['bottom_pos']
    down_bound = int(down_bound) + 100
    down_bound = int(down_bound)
    # print("调整完肺部的下界", down_bound)
    # print("开始调整")
    # 左右边界的
    right_pos = result_dict['right_pos']
    # print("肺部的右边界", right_pos)
    left_pos = result_dict['left_pos']
    # print("肺部的左边界", left_pos)
    middle_pos = (right_pos + left_pos) / 2
    right_bound = right_pos - 122
    left_bound = 122 - left_pos
    # 键鼠控制调整定位片的范围
    pull_locator_fixed(int(up_bound), int(down_bound))
    if right_bound >= left_bound:
        pull_locator_fixed_right(int(right_pos) + 30)
    else:
        pull_locator_fixed_left(int(left_pos) + 30)

    pull_locator_fixed_middle(int(middle_pos))

    return "范围调整完成"

def match_template(input_image_path):

    template_paths = [
        r"bed_right_or_wrong\SUCESS_after.jpg",
        r"bed_right_or_wrong\sucess1_after.jpg",
        r"bed_right_or_wrong\none_after.jpg"
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
            print("键鼠一切正常")
            result="键鼠一切正常"
            return result
        elif best_match_index == 1:

            print("开始将键盘切换成大写")
            KeyPress("CapsLock", 20, 40)
            id='SUCESS'
            input_patient_id(id)
            result ="键盘是小写已经将键盘切换成大写"
            return result
        elif best_match_index == 2:
            print("请人工检查键鼠转换器是否插紧")
            result = "请人工检查键鼠转换器是否插紧"
            return result
def count_bed_time():
    """计算移床时间
    """

    # 深度相机有时候返回的数值都是0，添加一个检测，来防止返回值都是0
    while True:
        point_distance, xiong_hou = deep_camera()
        if point_distance != 0 or xiong_hou != 0:
            print(f"point_distance: {point_distance}, xiong_hou: {xiong_hou}")
            break
        else:
            print("返回值都是0，重新尝试...")
            # 可以加一个延时，避免过于频繁的调用
            time.sleep(1)

    up_bed_height = (950 - xiong_hou / 2)
    up_bed_time = -8.20536825 + 0.0140479775 * up_bed_height + 0.00000696351319 * up_bed_height ** 2
    point_distance = -0.0003467404 * point_distance ** 3 + 0.1365383 * point_distance ** 2 - 17.9823 * point_distance + + 528.0566
    print("时间计算完成。升床用时：{}s，入床位置{}".format(up_bed_time, point_distance))
    pcb_up(up_bed_time)
    return "扫描床移动完成"

def system_check():
    info_dict = {}
    resetting()
    # #TODO 大门的自检 （需要人手动关门）
    # with open(r"D:\AgentAI_ls\golbal_door.txt", 'w', encoding='utf-8') as file:
    #     file.write("0\n")  # 写入数字 0
    #     # print("已将大门开和闭的数字调整到0")
    # #TODO 定位框的自检 （）
    # with open(r"D:\AgentAI_ls\golbal.txt", 'w', encoding='utf-8') as file:
    #     file.write("0\n")  # 写入数字 0
    #     # print("已将定位框的数字调整到0")
    # #TODO if_move_bed 自检
    # with open(r"D:\AgentAI_ls\if_move_bed.txt", 'w', encoding='utf-8') as file:
    #     file.write("0\n")  # 写入数字 0
    #     # print("已将是否移床的的数字调整到0")
    # #TODO Obs_if_use 自检
    # with open(r"D:\AgentAI_ls\Obs_if_use.txt", 'w', encoding='utf-8') as file:
    #     file.write("0\n")  # 写入数字 0
    #     # print("已将Obs是否占用的数字调整到0")

    #TODO 摄像头自检

    print("开始摄像头自检")
    try:
        url = 'http://192.168.1.195:5000/api/commom/'
        response1 = requests.get(url)
        print(f'普通摄像头接口传过来的数据：{response1.text}')
        info_dict["普通摄像头"] = "正常"
    except Exception as e:
        print("摄像头接口出现故障，请人工检查")
        info_dict["普通摄像头"] = "异常"
        print(f"错误信息: {str(e)}")  # 输出异常信息
        # 或者输出详细的堆栈信息
        print("详细错误信息：")
        traceback.print_exc()
    time.sleep(1)

    try:
        url = 'http://192.168.1.195:5000/api/deep/'
        response = requests.get(url)
        print(f'深度摄像头接口传过来的数据：{response.text}')
        info_dict["深度摄像头"] = "正常"
    except Exception as e:
        print("摄像头接口出现故障，请人工检查")
        info_dict["深度摄像头"] = "异常"
        print(f"错误信息: {str(e)}")  # 输出异常信息
        # 或者输出详细的堆栈信息
        print("详细错误信息：")
        traceback.print_exc()
    #TODO 调用升床和肺分割
    print("开始升床和肺分割自检")
    try:
        count_bed_time()
        info_dict["计算移床时间接口"] = "正常"
    except Exception as e:
        print("升床接口出现故障，请人工检查深度摄像头和控制面板继电器和IP是否正确")
        info_dict["计算移床时间接口"] = "异常"
        print(f"错误信息: {str(e)}")  # 输出异常信息
        # 或者输出详细的堆栈信息
        print("详细错误信息：")
        traceback.print_exc()
    try:
        adjust_range_scan()
        info_dict["调整定位片范围接口"] = "正常"
    except Exception as e:
        print("调整框接口出现问题，请人工检查算法IP和键鼠转换器是否松动")
        info_dict["调整定位片范围接口"] = "异常"
        print(f"错误信息: {str(e)}")  # 输出异常信息
        # 或者输出详细的堆栈信息
        print("详细错误信息：")
        traceback.print_exc()
    try:
        pcb_quit_bed()
        info_dict["退床接口"] = "正常"
    except Exception as e:
        button_close_all_system_check()
        info_dict["退床接口"] = "异常"
        print(f"错误信息: {str(e)}")  # 输出异常信息
        # 或者输出详细的堆栈信息
        print("详细错误信息：")
        traceback.print_exc()
    #TODO 门的开关自检

    print("开始开关门自检")
    baseurl = "https://www.lmcraft.com/lmiot/ctrl/sac07csa"
    params = {
        "api_key": "qJj8D8RqJU=kcYRtqtXDL2uSaVM=",
        "device_id": 1209858326,
        "op": "rs",
        "ch": 0,
        "param": 1
    }
    response = requests.get(baseurl, params=params)
    result = json.loads(response.text)
    if result["errno"] == 10:
        print("请人工将门控开关插上")
        info_dict["大门接口"] = "异常"
    else:
        time.sleep(5)
        #重新打开门，保证门状态和刚开始一样。
        baseurl = "https://www.lmcraft.com/lmiot/ctrl/sac07csa"
        params = {
            "api_key": "qJj8D8RqJU=kcYRtqtXDL2uSaVM=",
            "device_id": 1209858326,
            "op": "rs",
            "ch": 0,
            "param": 1
        }
        response = requests.get(baseurl, params=params)
        print("门的开关正常")
        info_dict["大门接口"] = "正常"


    #TODO 继电器的自检
    print("开始继电器自检")
    try:

        button_close_all_system_check()
        info_dict["继电器接口"] = "正常"
    except Exception as e:
        print("检查继电器是否通电，以及网线是否插上小主机")
        info_dict["继电器接口"] = "异常"
        print(f"错误信息: {str(e)}")  # 输出异常信息
        # 或者输出详细的堆栈信息
        print("详细错误信息：")
        traceback.print_exc()
    #TODO 键鼠自检

    print("开始键鼠自检")
    id='SUCESS'
    input_patient_id(id)
    get_picture_computer_HDMI()
    image_path = r'bed_right_or_wrong\captured_image_computer.jpg'
    result=match_template(image_path)
    info_dict["键鼠"] = result

    resetting()
    print(info_dict)
    # print("开始文件写入0")
    # with open(r"golbal_door.txt", 'w', encoding='utf-8') as file:
    #     file.write("0\n")  # 写入数字 0
    #     print("已将大门开和闭的数字调整到0")
    # #TODO 定位框的自检 （）
    # with open(r"golbal.txt", 'w', encoding='utf-8') as file:
    #     file.write("0\n")  # 写入数字 0
    #     print("已将定位框的数字调整到0")
    # #TODO if_move_bed 自检
    # with open(r"if_move_bed.txt", 'w', encoding='utf-8') as file:
    #     file.write("0\n")  # 写入数字 0
    #     print("已将是否移床的的数字调整到0")
    # #TODO Obs_if_use 自检
    # with open(r"Obs_if_use.txt", 'w', encoding='utf-8') as file:
    #     file.write("0\n")  # 写入数字 0
    #     print("已将Obs是否占用的数字调整到0")


def resetting():
    with open(r"txt/golbal_door.txt", 'w', encoding='utf-8') as file:
        file.write("0\n")  # 写入数字 0
        print("已将大门开和闭的数字调整到0")
    #TODO 定位框的自检 （）
    with open(r"txt/golbal.txt", 'w', encoding='utf-8') as file:
        file.write("0\n")  # 写入数字 0
        print("已将定位框的数字调整到0")
    #TODO if_move_bed 自检
    with open(r"txt/if_move_bed.txt", 'w', encoding='utf-8') as file:
        file.write("0\n")  # 写入数字 0
        print("已将是否移床的的数字调整到0")
    #TODO Obs_if_use 自检
    with open(r"txt/Obs_if_use.txt", 'w', encoding='utf-8') as file:
        file.write("0\n")  # 写入数字 0
        print("已将Obs是否占用的数字调整到0")

if __name__ == "__main__":
    # pass
    # while True:
    #     system_check()
    #     time.sleep(3)

    # import time
    # while True:
    #     print("开始键鼠自检")
    #     from ct_group.mk_control.mk_utils import input_patient_id
    #     id='SUCESS'
    #     input_patient_id(id)
    #     time.sleep(1)

    # system_check()
    # from ct_group.mk_control.mk_utils import input_patient_id
    # id='SUCESS'
    # input_patient_id(id)


    resetting()



