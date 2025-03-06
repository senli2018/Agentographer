import cv2
import datetime
import time
from tem_matching_input import match_template
from flask import Flask,jsonify
# 创建Flask应用实例
app = Flask(__name__)
def mapping(num):
    # 定义一个字典，键为数字，值为对应的界面内容
    interface_dict = {
        1: "患者信息输入界面",
        2: "输入进床深度和下界的界面",
        3: "定位片界面",
        4: "调整定位片范围界面",
        5: "正片扫描界面",
        6: "退床界面",
    }

    # 判断输入的数字是否在字典的键中
    if num in interface_dict:
        # 如果在，输出对应的界面内容
        print(interface_dict[num])
        return interface_dict[num]
    else:
        # 如果不在，提示输入错误
        print("不是规定的标准界面")
        return "No match found"

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

def get_screen():
    get_picture_computer_HDMI()
    image_path = 'voice_new/captured_image_computer.jpg'
    data_cv=match_template(image_path)
    data=mapping(data_cv)
    return data

# def get_screen_input_patient_info_flask():
#     for i in range(5):
#         data = get_screen()
#         if data == "患者信息输入界面":
#             print("成功获取到患者信息输入界面")
#             return "成功获取到患者信息输入界面"
#         else:
#             print("不是患者信息输入界面")
#     # 如果循环正常结束（未通过return提前退出），则返回未获取到界面的信息
#     return "尝试5次后仍未获取到患者信息输入界面"

@app.route('/get_screen', methods=['GET'])
def get_screen():
    data=get_screen()
    # 调用函数
    return jsonify({'message': data})
# 运行Flask应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

