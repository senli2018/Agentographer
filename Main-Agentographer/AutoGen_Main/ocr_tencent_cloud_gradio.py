import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
from CFG_GLOBAL import AGENT_RUN_DIR
import os
import datetime
import re
import cv2
import json
from PIL import Image, ImageEnhance
from datetime import datetime
import time


global_cap = None


def initialize_camera():
    global global_cap
    max_attempts = 3
    attempt = 0
    while attempt < max_attempts:
        try:
            if global_cap is not None:
                global_cap.release()
                global_cap = None

            global_cap = cv2.VideoCapture(1)
            if not global_cap.isOpened():
                print(f"Try {attempt + 1}/{max_attempts}: Unable to open video capture card")
                attempt += 1
                continue
            global_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1560)
            global_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            global_cap.set(cv2.CAP_PROP_FPS, 30)
            # 测试是否能够读取帧
            ret, _ = global_cap.read()
            if not ret:
                print(f"Try {attempt + 1}/{max_attempts}: The video frame cannot be read")
                attempt += 1
                continue
            print("The camera initialization succeeded. Procedure")
            return True
        except Exception as e:
            print(f"Try {attempt + 1}/{max_attempts}: Initialization error - {e}")
            attempt += 1
            if global_cap is not None:
                global_cap.release()
                global_cap = None
        time.sleep(1)
    print("The camera initialization failed. Procedure")
    return False


def release_camera():
    global global_cap
    if global_cap is not None:
        global_cap.release()
        global_cap = None


def enhance_image(input_path, output_path):
    image = Image.open(input_path)
    enhancer = ImageEnhance.Sharpness(image)
    image_enhanced = enhancer.enhance(2.0)
    contrast_enhancer = ImageEnhance.Contrast(image_enhanced)
    image_final = contrast_enhancer.enhance(1.5)
    image_final.save(output_path)


def get_picture_ocr():
    global global_cap
    if global_cap is None:
        print("The camera is not initialized")
        return None
    ret, frame = global_cap.read()
    if not ret:
        print("Unable to receive video frames")
        return None


    image_path = '.\img_temp\captured_image_ocr.jpg'
    cv2.imwrite(image_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print(f"The picture has been saved as {image_path}")
    enhance_image(image_path, image_path)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)
    return image


def tengxun():
    info_dict = {}
    try:
        # To instantiate an authentication object, enter it into Tencent cloud account SecretId and SecretKey, and pay attention to the confidentiality of the key pair
        # Keys can be obtain console to website https://console.cloud.tencent.com/cam/capiv
        cred = credential.Credential("xxxxx", "xxxxx")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "xxxx", clientProfile)  # Adding Region Parameters
        with open(r"img_temp\captured_image_ocr.jpg", "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode()
        req = models.GeneralAccurateOCRRequest()
        params = {
            "ImageBase64": base64_image
        }
        req.from_json_string(json.dumps(params))
        resp = client.GeneralAccurateOCR(req)
        print(resp.to_json_string())
        data = json.loads(resp.to_json_string())
        ocr_result = data
        text_data = [entry['DetectedText'] for entry in ocr_result['TextDetections']]
        full_text = ' '.join(text_data)
        print("The full text after splicing:")
        print(full_text)
        chinese_string = full_text
        no_space_string = chinese_string.replace(" ", "")
        print(no_space_string)
        patient_id_match = re.search(r'病人ID([A-Za-z0-9]+)',
                                     no_space_string)  # 病人ID 有可能因为干扰识别错误，搜索不到（可以拿到病人之后，空两个，再拿-也有可能出现ID少了，那么空两个也不太ok）
        if patient_id_match:
            patient_id = patient_id_match.group(1)
            print(f"病人ID: {patient_id}")
            info_dict["ID"] = patient_id
        else:
            print("病人ID信息未找到")
        name_match = re.search(r'姓名([^\W\d_]+?)(?=性别|出生|费别|\W|\d|_|[A-Za-z])', no_space_string)
        if name_match:
            name = name_match.group(1).strip()
            print(f"姓名: {name}")
            info_dict["Name"] = name
        else:
            print("姓名信息未找到")
        gender_match = re.search(r'性别(\w)', no_space_string)  # 性别的抗干扰能力需要提升 参照姓名的逻辑 此外除了姓名之外索也可以
        if gender_match:
            gender = gender_match.group(1)
            print(f"性别: {gender}")
            info_dict["Gender"] = gender
        else:
            print("性别信息未找到")

        if "胸部" in no_space_string:
            examination = "胸部CT平扫"
            info_dict["Examination"] = examination
        else:
            examination = "非胸部检查"
            info_dict["Examination"] = examination

        print(f"检查项目: {examination}")

        # 使用正则表达式找到出生或出生日期后边的四位数字
        birth_year_match = re.search(r'(出生|出生日期)(\d{4})', no_space_string)
        if birth_year_match:
            birth_year = birth_year_match.group(2)
            print(f"出生年份: {birth_year}")
            info_dict["年龄"] = birth_year
        else:
            print("出生年份信息未找到")

        if "住院号" in no_space_string:
            info_dict["体检与住院"] = "住院"
        else:
            info_dict["体检与住院"] = "体检"

        print(info_dict)

    except TencentCloudSDKException as err:
        print(err)

    return info_dict


def result_save(data):
    print(data)
    data_str = json.dumps(data, ensure_ascii=False)
    with open(os.path.join(AGENT_RUN_DIR,'data.txt'), 'a', encoding='utf-8') as file:
        file.write(data_str + '\n')
    print("数据已保存到data.txt文件中。")


def OcrRecognize_tengxun():
    get_picture_ocr()
    image_path = "./img_temp/captured_image_ocr.jpg"
    result = tengxun()
    result_save(result)
    return "{}已存到data.txt".format(result)


import gradio as gr


def run_ocr():
    return OcrRecognize_tengxun()


def load_data():
    try:
        with open("data.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "data.txt 文件未找到。"
    except UnicodeDecodeError:
        return "文件编码错误，无法读取文件内容。"


# 重新加载 data.txt 文件
def reload_data():
    return load_data()


# 使用 Gradio 构建界面
with gr.Blocks() as demo:
    # 初始化摄像头
    if not initialize_camera():
        raise RuntimeError("摄像头初始化失败")

    file_content_box = gr.Textbox(label="Loaded File Content", value=load_data())
    output_box = gr.Textbox(label="OCR Output")
    button = gr.Button("Generate")

    button.click(
        fn=lambda: (run_ocr(), reload_data()),
        inputs=[],
        outputs=[output_box, file_content_box]
    )

    # 添加程序结束时的清理代码
    demo.load(lambda: None, None, None).then(
        lambda: release_camera()
    )

demo.launch()