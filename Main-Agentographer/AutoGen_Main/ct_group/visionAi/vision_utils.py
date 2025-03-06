import cv2
from PIL import Image
from datetime import datetime
def get_picture_computer_HDMI():
    # 打开视频采集卡设备，假设设备索引为0
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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

    # 获取当前时间，并格式化为字符串
    currnt_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    #构造新的文件路径
    image_path = f'D://AgentAI_ls//iner_pic//captured_image_computer_{currnt_time}.jpg'
    cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print(f"图片已保存为 {image_path}")
    # 转换为PIL图像对象
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)
    # 释放资源
    cap.release()
    return image


#截屏屏幕的图片，然后裁剪图片的右下角，用于去模板匹配
def ocr_crop():
    import cv2
    from PIL import Image
    import time
    # 采集卡获取图片
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

    # 打开视频采集卡设备，假设设备索引为0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("无法打开视频采集卡")
        return None, None
    # 设置分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # 设置宽度
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # 设置高度
    # 读取第一帧视频

    # 等待相机初始化
    time.sleep(2)  # 增加延迟，等待相机准备好
    # 丢弃前几帧
    for _ in range(5):
        cap.read()
    ret, frame = cap.read()
    print(frame.shape)
    if not ret:
        print("无法接收视频帧（可能是视频流结束或者错误）")
        cap.release()
        return None, None
    # 保存图片并设置JPEG质量
    image_path = r'D:\Monitoring_AI\bed_right_or_wrong\bed.jpg'
    cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    # print(f"图片已保存为 {image_path}")
    with Image.open(image_path) as img:
        # 定义裁剪区域（左上角）
        # left = 960+960 - 438 + 100
        # top = 1000 - 80
        # right = 960+960 -100
        # bottom = 990
        left = 960+960 - 438
        top = 1000 - 80
        right = 960+960
        bottom = 990

        # 裁剪图像
        cropped_img = img.crop((left, top, right, bottom))
        output_image_path = r'D:\Monitoring_AI\bed_right_or_wrong\bed_resize.jpg'
        # 保存裁剪后的图像
        cropped_img.save(output_image_path)
    with Image.open(output_image_path) as img:
        # 再具体裁剪
        left = 220
        top = 20
        right = 280
        bottom = 50
        # 裁剪图像
        cropped_img = img.crop((left, top, right, bottom))
        output_image_path = r'D:\Monitoring_AI\bed_right_or_wrong\bed_resize.jpg'
        # 保存裁剪后的图像
        cropped_img.save(output_image_path)

    with open(r"D:\Monitoring_AI\txt\Obs_if_use.txt", 'w', encoding='utf-8') as file:
        file.write(f"0\n")

if __name__ == "__main__":
    pass
    # get_picture_computer_HDMI()
    # img=get_computer_camera()
    # get_picture_computer_HDMI()
    # get_picture_side()
    # get_picture_computer_HDMI()
    #img.show()
    # get_picture_side()
    # get_picture_up()
    # get_picture_side()
    # deep_camera()
    ocr_crop()
    # ocr_crop_info()
    # ocr_crop_middle_picture()
    # get_picture_computer_HDMI()
    # get_computer_camera_sideocr()
    # get_computer_camera()
    # get_picture_computer_HDMI()
    # ocr_crop_middle_picture1111()