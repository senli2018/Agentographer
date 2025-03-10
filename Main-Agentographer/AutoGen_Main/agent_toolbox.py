#  所有的function call 都在这里 agent运行时，会调用这里。
import os.path
import threading
import pygame
import time
import datetime
import json
import requests
import pyttsx3
from CFG_GLOBAL import AGENT_RUN_DIR
def input_patient_info():
    """输入患者检查项目
    """
    from pypinyin import pinyin, Style
    from ct_group.mk_control.mk_utils import input_patient_id, input_patient_name, input_patient_age, input_patient_sex, \
        patient_chest_button_low, patient_chest_button_high, input_patient_hight, input_patient_weight, MoveTo, shut_down_skyeyes
    from ct_group.patientinfo.patient_utils import read_first_line
    from ct_group.mk_control.mk_utils import patient_check
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[输入患者检查项目]", start_session_time)
    process_start_session_time = time.strftime("检查开始时间" + '%Y年%m月%d日 %H点%M分%S秒', start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    filename1 = os.path.join(AGENT_RUN_DIR,'txt/process_time.txt')
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    with open(filename1, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(process_start_session_time + '\n')
    start_time = datetime.datetime.now()
    print("Manually input the information of the patient's left side.")
    # 读取data.txt文件的第一行信息
    data = read_first_line()
    patient_info = json.loads(data)
    id = patient_info["ID"]
    # TODO 将姓名转为大写拼音
    name = patient_info["Name"]
    # TODO 同时呼叫患者的名字
    def call_patient(name):
        str_voice = f"请{name}进入扫描间"
        # str_voice1 ="接下来请您听语音指示"
        engine = pyttsx3.init()
        engine.setProperty('rate', 138)  # 设置语速
        engine.say(str_voice)
        time.sleep(1)
        engine.runAndWait()
        print("playground：{}".format(str_voice))
    # 创建并启动播放音频的线程
    thread_call_patient = threading.Thread(target=call_patient, args=(name,))
    thread_call_patient.start()
    pinyin_name = pinyin(name, style=Style.NORMAL)
    # 将拼音列表转换为字符串，并转换为大写
    name = ' '.join([word[0] for word in pinyin_name]).upper()
    age = patient_info['年龄']
    age = age[:4]
    age = 2024 - int(age)
    sex = patient_info["Gender"]
    part = "胸部平扫"
    # 输入患者的ID
    input_patient_id(id)
    time.sleep(0.5)
    # 输入患者的名字
    pinyin_name = pinyin(name, style=Style.NORMAL)
    # 将拼音列表转换为字符串，并转换为大写
    name = ' '.join([word[0] for word in pinyin_name]).upper()
    input_patient_name(name)
    time.sleep(0.5)
    # 输入患者的年龄
    input_patient_age(str(age))
    time.sleep(0.5)
    # 输入患者的身高
    hight = "165"
    # hight=patient_info["身高"]
    # input_patient_hight(hight)
    time.sleep(0.5)
    # 输入患者的体重
    weight = "65"
    # weight=patient_info["体重"]
    # input_patient_weight(weight)
    time.sleep(0.5)   # 输入患者的性别
    input_patient_sex(sex)
    time.sleep(0.5)
    # 输入患者的扫描部位，，目前只是进行胸部平扫
    type = patient_info["体检与住院"]
    if str(type)=="体检":
        patient_chest_button_low()
    else:
        patient_chest_button_high()
    time.sleep(1)
    patient_check()
    time.sleep(1)
    shut_down_skyeyes()
    voice_new_12()
    time.sleep(2)
    # voice_new_14()
    str_voice = f"请您脱掉帽子，请您头躺进头托里"
    # print("播报：{}".format(str_voice))
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # 设置语速
    engine.say(str_voice)
    engine.runAndWait()
    time.sleep(2.5)
    filename = os.path.join(AGENT_RUN_DIR,"txt/datatime.txt")
    return "患者信息已输入完成"
def open_door():
    """打开扫描间舱门
    """
    start_session_time=time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒'+":action[打开扫描间舱门]",start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    print(filename0)
    #TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    global_var2 = 1
    with open(os.path.join(AGENT_RUN_DIR,"txt/golbal_door.txt"), "w", encoding="utf-8") as file:
        file.write(f"{global_var2}\n")
    # 输出开始时间
    start_time = datetime.datetime.now()
    print("open the door")
    baseurl = ""
    params = {
        "api_key": "qJj8D8RqJU=kcYRtqtXDL2uSaVM=",
        "device_id": 1209858326,
        "op": "rs",
        "ch": 0,
        "param": 1
    }
    # 检测舱门时候打开成功，如果打开失败，则重现调用舱门打开的请求
    while True:
        response = requests.get(baseurl, params=params)
        result = json.loads(response.text)
        if result["errno"] == 10:
            print("The cabin door failed to open. Try again...")
        else:
            print("The cabin door has been opened successfully.")
            break
    return "舱门打开完成"
def speak_voice(voice: str):
    """播放语音

        Args:
            voice(str): 语音内容
    """
    # 输出开始时间
    print("playground：{}".format(voice))
    engine = pyttsx3.init()
    engine.setProperty('rate', 138)  # 设置语速
    engine.say(voice)
    engine.runAndWait()
    return "播报成功"
def count_bed_time():
    """计算移床时间
    """
    from ct_group.ct_control.ct_utils import pcb_up
    from pose_request.position_request import deep_camera
    from thread_utils import sure_patient_info
    from http.client import RemoteDisconnected
    from ct_group.mk_control.mk_utils import input_inbed_positon,pull_point
    from ct_group.ct_control.ct_utils import pcb_one_click
    from ct_group.mk_control.mk_utils import input_inbed_positon_have_button
    start_session_time=time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒'+":action[计算移床时间]",start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    #TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    # 输出开始时间
    start_time = datetime.datetime.now()
    print("Program start time:", start_time)
    failure_count = 0
    # 设置最大失败次数
    max_failures = 5
    while True:
        try:
            point_distance, xiong_hou,end_point = deep_camera()
            if point_distance != 0 or xiong_hou != 0:
                print(f"point_distance: {point_distance}, xiong_hou: {xiong_hou}")
                break
            else:
                print("The return values are all 0. Please try again...")
                time.sleep(1)
        except (requests.exceptions.ConnectionError, RemoteDisconnected) as e:
            print(f"An abnormality occurred.：{e}")
            failure_count += 1
            if failure_count >= max_failures:
                print("Three attempts have failed and manual takeover is required.")
                break
            else:
                print("Trying to reconnect...")
                time.sleep(2)

    from pose_request.position_request import append_to_txt_file
    with open("data_finsh.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if lines:
            patient_name_file = lines[-1].strip()  # 获取最后一行并去除首尾空格

    patient_name_file = json.loads(patient_name_file)
    print(patient_name_file)

    # 假设患者名字存储在patient_name.txt文件中
    ID = patient_name_file["ID"]
    print(ID)
    # 指定要写入的文件名
    filename = r"txt/height_and_in_data.txt"
    append_to_txt_file(ID, xiong_hou/2, filename)
    up_bed_height = (950 - xiong_hou / 2)
    up_bed_time = -8.20536825 + 0.0140479775 * up_bed_height + 0.00000696351319 * up_bed_height ** 2
    point_distance = -0.0003467404 * point_distance ** 3 + 0.1365383 * point_distance ** 2 - 17.9823 * point_distance + + 528.0566
    #人为设定了模拟值
    if int(-point_distance)>400:
        point_distance=-300
    else:
        point_distance=point_distance
    print("The time calculation is completed. The time taken for bed elevation is {} seconds, and the position of the bed when entering the room is {}.".format(up_bed_time, point_distance))
    print("正在移动扫描床")
    audio_thread = threading.Thread(target=sure_patient_info)
    audio_thread.start()
    pcb_up(up_bed_time)
    # 等待音频播放线程结束
    audio_thread.join()
    pull_point(end_point)
    time.sleep(1)
    # 在显示器上用键鼠输入进床信息
    input_inbed_positon(point_distance)
    #判断输入信息是否出错
    input_inbed_positon(point_distance)
    # 然后重新去坐标输入
    input_inbed_positon_have_button()
    time.sleep(1.5)
    print("Start one-click bed transfer.")
    pcb_one_click()
    return "扫描床移动完成"

def Pub_one_click():
    """一键移床
    """
    from ct_group.ct_control.ct_utils import pcb_one_click
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[一键移床]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    pcb_one_click()
    return "开始一键移床"
def delayed(num: int):
    """延时，延迟num秒

        Args:
            num(int): 延时num秒
    """

    time.sleep(num)
    return "延时已完成"
def pose_film_scanning():
    """定位片扫描
    """
    from ct_group.ct_control.ct_utils import pcb_scan
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[定位片扫描]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')

    pcb_scan()
    return "定位片扫描完成"
def adjust_range_scan():
    """调整定位片范围
    """
    from pose_request.position_request import ct_seg_request
    from ct_group.mk_control.mk_utils import pull_locator_fixed, pull_locator_fixed_left, pull_locator_fixed_right, \
        pull_locator_fixed_middle
    from ct_group.visionAi.vision_utils import get_picture_computer_HDMI
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[调整定位片范围]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    filename = os.path.join(AGENT_RUN_DIR,"txt/datatime.txt")
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')


    # 采集卡获取图片
    while True:
        with open(os.path.join(AGENT_RUN_DIR,"txt/Obs_if_use.txt"), 'r', encoding='utf-8') as file:
            lines = file.readlines()
            text = lines[0].strip()  # 读取第一行并去除可能的空白字符
        if int(text) == 0:
            with open(os.path.join(AGENT_RUN_DIR,"txt/Obs_if_use.txt"), 'w', encoding='utf-8') as file:
                file.write(f"1\n")
            break
        else:
            print("Wait for 0.5 seconds. Other devices will be released for use after this period.")
            time.sleep(0.5)

    data = get_picture_computer_HDMI()
    with open(os.path.join(AGENT_RUN_DIR,"txt/Obs_if_use.txt"), 'w', encoding='utf-8') as file:
        file.write(f"0\n")
    # 初始化失败次数计数器
    failure_count = 0
    # 设置最大失败次数
    max_failures = 3

    while True:
        try:
            result_data = ct_seg_request(data)
            print("Request successful. Processing result:", result_data)
            break
        except Exception as e:
            print(f"Error occurred:{e}")
            failure_count += 1
            if failure_count >= max_failures:
                print("Three attempts have failed and manual takeover is required.")
                break
            else:
                print("Try to re-request...")
                time.sleep(1)
    result_dict = json.loads(result_data)
    up_bound = result_dict['top_pos']
    print("The upper boundary of the lungs", int(up_bound))
    up_bound = int(up_bound) - 40
    up_bound = int(up_bound)
    print("Adjust the upper boundary of the lungs", up_bound)
    down_bound = result_dict['bottom_pos']
    print("The lower boundary of the lungs", int(down_bound))
    down_bound = int(down_bound) + 100
    down_bound = int(down_bound)
    print("Adjust the lower boundary of the lungs", down_bound)
    # 左右边界的
    right_pos = result_dict['right_pos']
    print("The right boundary of the lungs", right_pos)
    left_pos = result_dict['left_pos']
    print("The left boundary of the lungs", left_pos)
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

    print("The range of the positioning film has been adjusted.")

    global_var = 1
    with open(os.path.join(AGENT_RUN_DIR,"txt/golbal.txt"), "w", encoding="utf-8") as file:
        file.write(f"{global_var}\n")
    print("Have you completed the adjustment of the frame range?：",global_var)
    user_input = input("The doctor checks whether the adjustment box is accurate and inputs 0 to continue the execution of the program.")
    if user_input == "0":
        print("The doctor has completed the confirmation and the procedure can proceed.")
    return "The scope adjustment has been completed."
def positive_film_scanning():
    """正片扫描
    """
    from ct_group.ct_control.ct_utils import pcb_one_click, pcb_scan
    from ct_group.mk_control.mk_utils import yes_button_1
    from ct_group.patientinfo.ocr_camera import ocr_inital, ocr_scan_complete, ocr_inital_oneclick_to_scan
    from ct_group.mk_control.mk_utils import yes_button2
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[正片扫描]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    # 输出开始时间
    start_time = datetime.datetime.now()
    print("Program start time:", start_time)
    # 点击确认按钮
    yes_button_1()
    # 利用图像匹配，判断是否初始化完成
    print("Check whether the initialization is completed")
    ocr_inital()
    print("Initialization has been completed.")
    print("Start one-click bed transfer.")
    # 一键移床和一键扫描
    pcb_one_click()
    print("Determine whether one-click scanning is feasible.")
    ocr_inital_oneclick_to_scan()
    time.sleep(1)
    print("Start one-click scanning")
    pcb_scan()
    # 等待5s确保扫描完毕
    print("Determine whether the bed-check-out interface appears")
    ocr_scan_complete()
    print("The check-out interface has already appeared.")
    print("The original film has been scanned.")
    return "正片扫描完成"

def hold_get_out_bed():
    """扫描床归位
    """
    from ct_group.ct_control.ct_utils import pcb_quit_bed
    from ct_group.mk_control.mk_utils import yes_button2
    from thread_utils import play_audio, quit_bed
    from ct_group.patientinfo.patient_utils import save_dict
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[扫描床归位]", start_session_time)
    # 指定要写入的文件名
    filename1 = os.path.join(AGENT_RUN_DIR,'txt/process_time.txt')
    new_filename = os.path.join(AGENT_RUN_DIR,'txt/function_time_copy.txt')
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')

    global_var = 0
    with open(os.path.join(AGENT_RUN_DIR,"txt/golbal.txt"), "w", encoding="utf-8") as file:
        file.write(f"{global_var}\n")

    start_time = datetime.datetime.now()
    print("Program start time:", start_time)

    # 正片扫描完成后的完成按钮
    yes_button2()
    time.sleep(1)
    yes_button2()
    print("程序开始时间:", start_time)

    # 创建并启动播放音频的线程
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()
    # 执行退床操作
    quit_bed()
    # 等待音频播放线程结束
    audio_thread.join()
    # 弹出对话框，判断是否执行开舱门逻辑
    with open(os.path.join(AGENT_RUN_DIR,"txt/if_move_bed.txt"), "w", encoding="utf-8") as file:
        file.write("0\n")  # 写入数字 0 ，表示姿势是否标准，0代表不标准

    with open(os.path.join(AGENT_RUN_DIR,"txt/voice_times.txt"), 'w', encoding='utf-8') as file:
        file.write("0\n") #写入数字 0，表示 是播报请家属出去等，还是请家属门外等候。
    #TODO 手动控制门的开和关，主要是人为判断人是否穿好了衣服
    time.sleep(2)
    open_door()
    # user_input = input("是否执行开舱门操作？输入 1 执行，输入 0 跳过：")
    # if user_input == "1":
    #     open_door()
    # elif user_input == "0":
    #     print("跳过开舱门操作，流程结束")
    # else:
    #     print("输入无效，默认跳过开舱门操作")
    print("扫描床归位完成")

    process_start_session_time = time.strftime("检查结束时间" + '%Y年%m月%d日 %H点%M分%S秒', start_session_time)
    # TODO 将项目的结束时间写入
    with open(filename1, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(process_start_session_time + '\n')

    #将function call 记录到process_time.txt文件中
    save_dict()
    #将此次患者的function call全部记录到 process_time.txt文件中，然后将信息保存到新的备份文件中function_time_copy.txt，将原有的function_time.txt清空

    # 步骤1: 读取原始文件的内容
    with open(filename0, 'r', encoding='utf-8') as source_file:
        content = source_file.read()

    # 步骤3: 将读取的内容写入新文件
    with open(new_filename, 'a', encoding='utf-8') as new_file:
        new_file.write(content + '\n')

    # 步骤4: 清空原始文件的内容
    with open(filename0, 'w', encoding='utf-8') as source_file:
        source_file.write('')
    return "扫描床归位完成"
def ctimage_analysis(name,sex,age,check,dicom_path):
    """肺结节预测报告诊断

        Args:
            name(str)      :姓名
            sex(str)       :性别
            age(int)       :年龄
            check(str)     :部位
            dicom_path(str):影像路径
    """
    from llma import call_llama_api
    url = "http://localhost:8000/api/pami/v1/nodule_detection"
    files = {'dicom': (dicom_path, open(dicom_path, 'rb'))}
    response = requests.post(url, files=files)

    combined_data = [
        {"role": "user",
         "content": {
                        "name": name,
                        "sex": sex,
                        "age": age,
                        "check": check,
                        "nodule_info": response,
                        "prompt": "请根据以上的信息，生成一份中文肺癌筛查诊断报告"}
         }
    ]
    #利用本地训练的大模型
    data = call_llama_api(combined_data)
    return data
def close_door():
    """关闭舱门
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[关闭舱门]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    global_var2 = 0
    with open(os.path.join(AGENT_RUN_DIR,"txt/golbal_door.txt"), "w", encoding="utf-8") as file:
        file.write(f"{global_var2}\n")
    # 输出开始时间
    start_time = datetime.datetime.now()
    print("程序开始时间:", start_time)
    print("舱门关闭")

    # 请求的路径和参数
    baseurl = ""
    params = {
        "api_key": "qJj8D8RqJU=kcYRtqtXDL2uSaVM=",
        "device_id": 1209858326,
        "op": "rs",
        "ch": 0,
        "param": 1
    }
    # 检测舱门是否关闭成功，如果关闭失败，则重现调用舱门关闭的请求
    while True:
        response = requests.get(baseurl, params=params)
        result = json.loads(response.text)

        if result["errno"] == 10:
            print("舱门关闭失败，重新尝试...")
        else:
            print("舱门关闭成功")
            break
    print("舱门关闭完成")
    # 输出结束时间
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    filename = os.path.join(AGENT_RUN_DIR,"txt/datatime.txt")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"关闭舱门接口起始时间: {start_time}\n")
        file.write(f"关闭舱门位接口结束时间: {end_time}\n")
        file.write(f"关闭舱门时间: {end_time - start_time}\n")
        file.write("-" * 40 + "\n")  # 分隔线
    time.sleep(6)
    return "关闭舱门成功"
def task_over():
    """任务结束
    """
    from ct_group.ct_control.ct_utils import button_close_all
    button_close_all()
    print("任务结束")
    return "TERMINATE"
def voice_1():
    """双臂交叉向头顶伸直
    """
    current_time = time.strftime('%H点%M分%S秒' + ":action[双臂交叉向头顶伸直]", time.localtime())
    filename = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("双臂交叉，向头顶伸直")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice/Keep your arms crossed and straight above your head.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_2():
    """胳膊抱住头
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[胳膊抱住头]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("胳膊抱住头")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice/Wrap one arms around one head.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_3():
    """请上交预约单等舱门打开后进入扫描间
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请上交预约单等舱门打开后进入扫描间]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请上交预约单，等舱门打开后进入扫描间")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(
        r'voice/Please hand in the reservation form and enter the scanning room when the cabin door is opened.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()

    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_4():
    """请家属及无关人员去扫描间外等候
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请家属及无关人员去扫描间外等候]",
                                 start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请家属及无关人员去扫描间外等候")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice/Please wait outside the scanning room.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_5():
    """请您不要动检查马上就好了
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请您不要动检查马上就好了]",
                                 start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请您不要动，检查马上就好了")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice/Please don')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_6():
    """请穿好衣服拿好随身物品回去等检查报告结果
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请穿好衣服拿好随身物品回去等检查报告结果]",
                                 start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请穿好衣服，拿好随身物品，回去等检查报告结果")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(
        r'voice/Please get dressed, take your belongings, and wait for the results of the inspection report.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_7():
    """请脱掉外套摘掉身上的金属制品
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请脱掉外套摘掉身上的金属制品]",
                                 start_session_time)
    # 指定要写入的文件名
    filename0 =os.path.join(AGENT_RUN_DIR, 'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请脱掉外套，摘掉身上的金属制品")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice/Please take off your coat and any metalwork.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_8():
    """请躺在扫描床上头躺进头托里
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请躺在扫描床上头躺进头托里]",
                                 start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请躺在扫描床上，头躺进头托里")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice/Please lie on the scanning bed with your head in the headrest.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_1():
    """不用摘眼镜
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[不用摘眼镜]",start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("不用摘眼镜")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new/Don')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()

    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_2():
    """不要动检查马上结束
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[不要动检查马上结束]",start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("不要动检查马上结束")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new/Don')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_3():
    """检查完成请您回去等检查报告结果
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[检查完成请您回去等检查报告结果]",start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("检查完成请您回去等检查报告结果")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new/Please go back and wait for the result of the inspection report.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_4():
    """请不要动
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请不要动]",start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请不要动")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new/Please don')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_5():
    """请双臂往中间收
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请双臂往中间收]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请双臂往中间收")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new/Keep your arms in the middle, please.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()

    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_7():
    """请放下包包
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请放下包包]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请放下包包")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new/Please put down your bag.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_8():
    """请躺在床上头躺进头托里脱掉鞋子
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请躺在床上头躺进头托里脱掉鞋子]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请躺在床上头躺进头托里脱掉鞋子")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new\请躺在床上头躺进头托里脱掉鞋子.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_9():
    """请进入扫描间
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请进入扫描间]",start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请进入扫描间")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new\请进入扫描间.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_10():
    """请家属出去等
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请家属出去等]",start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')

    with open(os.path.join(AGENT_RUN_DIR,"txt/voice_times.txt"), 'r', encoding='utf-8') as file:
        lines = file.readlines()
        text = lines[0].strip()  # 读取第一行并去除可能的空白字符
        text =int(text)
    # 次数加1
    text += 1
    # 将更新后的数值写回文件
    with open(os.path.join(AGENT_RUN_DIR,"txt/voice_times.txt"), 'w', encoding='utf-8') as file:
        file.write(str(text))
    start_time = datetime.datetime.now()
    print("请家属出去等")
    print("pygame程序开始时间:", start_time)
    if text < 3:
        # 初始化pygame
        pygame.init()
        # 加载音频文件
        pygame.mixer.init()
        pygame.mixer.music.load(r'voice_new/Please ask the family to wait outside.mp3')
        # 播放音频
        pygame.mixer.music.play()
        # 等待音频播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        # 退出pygame
        pygame.quit()
    else:
        # 初始化pygame
        pygame.init()
        # 加载音频文件
        pygame.mixer.init()
        pygame.mixer.music.load(r'voice_new\请家属门外等候.mp3')
        # 播放音频
        pygame.mixer.music.play()
        # 等待音频播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        # 退出pygame
        pygame.quit()

    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_11():
    """请脱掉鞋子
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请脱掉鞋子]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请脱掉鞋子")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new/Please take off your shoes.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()

    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_12():
    """请去调胸前的金属物品躺在床上头躺在头托里鞋子脱掉
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请去调胸前的金属物品躺在床上头躺在头托里鞋子脱掉]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请去调胸前的金属物品躺在床上头躺在头托里鞋子脱掉")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new\请去掉外套.mp3')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_13():
    """请您双手抱头
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请您双手抱头]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')

    start_time = datetime.datetime.now()
    print("请您双手抱头")
    print("pygame程序开始时间:", start_time)
    # 初始化失败次数计数器
    failure_count = 0
    # 设置最大失败次数
    max_failures = 3

    while True:
        try:
            # url = "http://192.168.1.141:5000/play?action=2"
            # response = requests.get(url)
            str_voice = f"请您双手抱头"
            # print("播报：{}".format(str_voice))
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)  # 设置语速
            engine.say(str_voice)
            engine.runAndWait()
            break
            # 检查响应状态码是否为200，即请求成功
        except requests.exceptions.RequestException as e:
            # 捕获请求异常，如连接错误、超时等
            print(f"请求异常：{e}")
            failure_count += 1
            if failure_count >= max_failures:
                print("三次尝试失败，需要人工接管。")
                break
            else:
                print("尝试重新请求...")
                time.sleep(1)

    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    time.sleep(5)
    return "播报完毕"
def voice_new_14():
    """视频动作1
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime( '%H点%M分%S秒' + ":action[请您头躺进头托里]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')

    start_time = datetime.datetime.now()
    print("请您头躺进头托里")
    print("pygame程序开始时间:", start_time)
    # 初始化失败次数计数器
    failure_count = 0
    # 设置最大失败次数
    max_failures = 3

    while True:
        try:
            url = ""
            response = requests.get(url)
            break
            # 检查响应状态码是否为200，即请求成功
        except requests.exceptions.RequestException as e:
            # 捕获请求异常，如连接错误、超时等
            print(f"请求异常：{e}")
            failure_count += 1
            if failure_count >= max_failures:
                print("三次尝试失败，需要人工接管。")
                break
            else:
                print("尝试重新请求...")
                time.sleep(1)

    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_15():
    """请把项链往上提其他别动
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime('%H点%M分%S秒' + ":action[请把项链往上提其他别动]", start_session_time)
    # 指定要写入的文件名
    filename0 =os.path.join(AGENT_RUN_DIR, 'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')
    start_time = datetime.datetime.now()
    print("请把项链往上提其他别动")
    print("pygame程序开始时间:", start_time)
    # 初始化pygame
    pygame.init()
    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new/Please lift the necklace up and don')
    # 播放音频
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    # 退出pygame
    pygame.quit()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"
def voice_new_16():
    """视频动作1加上其他视频
    """
    start_session_time = time.localtime()
    # 获取当前时间
    current_time = time.strftime( '%H点%M分%S秒' + ":action[请您头躺进头托里]", start_session_time)
    # 指定要写入的文件名
    filename0 = os.path.join(AGENT_RUN_DIR,'txt/function_time.txt')
    # TODO 将function call调用时间写入
    with open(filename0, 'a', encoding='utf-8') as file:
        # 将当前时间写入文件，并添加换行符
        file.write(current_time + '\n')

    start_time = datetime.datetime.now()
    print("请您头躺进头托里")
    print("pygame程序开始时间:", start_time)
    # 初始化失败次数计数器
    failure_count = 0
    # 设置最大失败次数
    max_failures = 3
    #TODO 加上条件判读  查看
    url = 'http://192.168.1.195:5000/api/gptpost/' # 人数由2080做判断返回结果
    response = requests.get(url)
    print(f"判断患者是否躺在托里的数据: {response.text}")
    data_video = json.loads(response.text)
    if int(data_video)==1:
        while True:
            try:
                url = ""
                response = requests.get(url)
                break
                # 检查响应状态码是否为200，即请求成功
            except requests.exceptions.RequestException as e:
                # 捕获请求异常，如连接错误、超时等
                print(f"请求异常：{e}")
                failure_count += 1
                if failure_count >= max_failures:
                    print("三次尝试失败，需要人工接管。")
                    break
                else:
                    print("尝试重新请求...")
                    time.sleep(1)
    else:
        str_voice = f"请向上躺,头躺进头托里"
        engine = pyttsx3.init()
        engine.setProperty('rate', 138)  # 设置语速
        engine.say(str_voice)
        engine.runAndWait()
    end_time = datetime.datetime.now()
    print("程序结束时间:", end_time)
    # 计算并输出程序运行时间
    elapsed_time = end_time - start_time
    print("程序运行时间:", elapsed_time)
    return "播报完毕"

if __name__ == "__main__":
    pass
    # input_patient_info()
    # voice_1()
    # speak_voice_name()





















