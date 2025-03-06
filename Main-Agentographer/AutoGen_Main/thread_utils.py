def play_audio():
    """播放音频"""
    import time
    import pygame
    #等床下降的差不多了，再播放语音
    time.sleep(9)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(r'voice_new/The inspection has been completed..mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    pygame.quit()
def quit_bed():
    """一键退床操作"""
    from ct_group.ct_control.ct_utils import pcb_quit_bed
    pcb_quit_bed()


def sure_patient_info():
    """播放音频"""
    # 读取txt文件的最后一行以获取患者的名字
    import json
    import pyttsx3
    with open("data_finsh.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if lines:
            patient_name_file = lines[-1].strip()  # 获取最后一行并去除首尾空格
    patient_name_file = json.loads(patient_name_file)
    # 假设患者名字存储在patient_name.txt文件中
    patient_name = patient_name_file["Name"]
    print(patient_name)
    # 播报内容
    str_voice = f"请问你是{patient_name}吗，如果不是请举手。"
    print("播报：{}".format(str_voice))
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # 设置语速
    engine.say(str_voice)
    engine.runAndWait()

if __name__ == "__main__":
    sure_patient_info()