import ctypes
import time
from ct_group.config import device_cfg

com = device_cfg.mk_com
kmdll = ctypes.CDLL('D:\Monitoring_AI\ct_group\mk_control\ddll64.dll')

com_bytes = com.encode('utf-8')
ret = kmdll.OpenDevice(ctypes.c_char_p(com_bytes))
kmdll.SetScreenScale(1920, 1080)


def KeyDown(keyname: str):
    """按下键盘按键

        Args:
            keyname(str): 键盘字母或数字
    """
    kmdll.KeyDownName(ctypes.c_char_p(bytes(keyname, "utf-8")))
    time.sleep(0.002)
    return "键盘按下{}键成功".format(keyname)

def KeyUp(keyname: str):
    """抬起键盘按键

        Args:
            keyname(str): 键盘字母或数字
    """
    kmdll.KeyUpName(ctypes.c_char_p(bytes(keyname, "utf-8")))
    time.sleep(0.002)
    return "键盘抬起{}键成功".format(keyname)


def KeyPress(keyname: str, min: int, max: int):
    """按下并抬起键盘按键

        Args:
            keyname(str): 键盘字母或数字
            min(int): 最小延时
            max (int): 最大延时
    """
    kmdll.KeyPressName(ctypes.c_char_p(bytes(keyname, "utf-8")), min, max)
    time.sleep(0.002)
    return "键盘按下并抬起{}键成功".format(keyname)


def SayString(s: str, min: int, max: int):
    """输入键盘字符串

    Args:
        s (str): 键盘字符串
        min (int): 最小延时
        max (int): 最大延时
    """
    kmdll.SayString(ctypes.c_char_p(s.encode(encoding="utf-8")), min, max)
    return "键盘输入{}成功".format(s)


def MoveTo(x: int, y: int):
    """将鼠标绝对移动到指定坐标

    Args:
        x (int): x坐标
        y (int): y坐标
    """
    kmdll.MoveTo(x, y)
    time.sleep(0.001)
    return "鼠标移动到({},{})成功".format(x, y)


def MoveTo_str(x: str, y: str):
    """将鼠标绝对移动到指定坐标

    Args:
        x (str): x坐标
        y (str): y坐标
    """
    kmdll.MoveTo(x, y)
    time.sleep(0.001)
    return "鼠标移动到({},{})成功".format(x, y)


def MoveR(dx: int, dy: int):
    """将鼠标相对移动特定距离

    Args:
        dx (int): x方向偏移像素
        dy (int): y方向偏移像素
    """
    kmdll.MoveR(dx, dy)
    time.sleep(0.001)
    return "鼠标相对移动({},{})成功".format(dx, dy)


def LeftDown():
    """按住左键"""
    kmdll.LeftDown()
    time.sleep(0.002)
    return "鼠标左键按下成功"


def LeftUp():
    """抬起左键"""
    kmdll.LeftUp()
    time.sleep(0.002)
    return "鼠标左键抬起成功"


def LeftClick(min: int = 50, max: int = 120):
    """左键单击

    Args:
        min (int, optional): 最短延时. Defaults to 50.
        max (int, optional): 最长延时. Defaults to 120.
    """
    kmdll.LeftClick(min, max)
    return "鼠标左键单击成功"


def LeftDoubleClick(min: int = 50, max: int = 120):
    """左键双击

    Args:
        min (int, optional): 最短延时. Defaults to 50.
        max (int, optional): 最长延时. Defaults to 120.
    """
    kmdll.LeftDoubleClick(min, max)
    time.sleep(0.002)
    return "鼠标左键双击成功"


def RightDown():
    """按住右键
    """
    kmdll.RightDown()
    time.sleep(0.002)
    return "鼠标右键按下成功"


def RightUp(self):
    """抬起右键
    """
    kmdll.RightUp()
    time.sleep(0.002)
    return "鼠标右键抬起成功"


def RightClick(min: int = 50, max: int = 120):
    """右键单击"""
    kmdll.RightClick(min, max)
    time.sleep(0.002)
    return "鼠标右键单击成功"


def MouseWheel(delta: int = -120):
    """滚动鼠标滚轮

    Args:
        delta (int): 滚动距离，正数向上，负数向下
    """
    kmdll.MouseWheel(delta)
    return "鼠标滚轮滚动{}成功".format(delta)


# =====================
def input_patient_id(id: str):
    # 屏幕尺寸1920， 1080
    # 患者编号位置
    MoveTo(1920 // 2 + 100, 160)
    LeftClick(50, 120)
    KeyDown("Ctrl")
    KeyPress("A", 20, 40)
    KeyUp("Ctrl")
    time.sleep(0.002)
    KeyPress("BackSpace", 20, 40)
    KeyDown("CapsLock")
    time.sleep(0.002)
    KeyUp("CapsLock")
    SayString(id, 20, 40)
    KeyDown("CapsLock")
    time.sleep(0.002)
    KeyUp("CapsLock")
    print("id输入成功， 人为延时")
    # time.sleep(3)


def input_patient_name(name: str):
    # # 姓名位置
    MoveTo(1920 // 2 + 100, 200)
    LeftClick(50, 120)
    KeyDown("Ctrl")
    KeyPress("A", 20, 40)
    KeyUp("Ctrl")
    # KeyPress("BackSpace", 20, 40)
    KeyPress("Delete", 20, 40) # 使用delete
    KeyDown("CapsLock")
    time.sleep(0.002)
    KeyUp("CapsLock")
    SayString(name, 20, 40)
    KeyDown("CapsLock")
    time.sleep(0.002)
    KeyUp("CapsLock")
    print("姓名输入成功，人为延时")


def input_patient_age(age: str):
    # 年龄位置
    MoveTo(1920 // 2 + 100, 240)
    LeftClick(50, 120)
    KeyDown("Ctrl")
    KeyPress("A", 20, 40)
    KeyUp("Ctrl")
    KeyPress("BackSpace", 20, 40)
    SayString(age, 20, 40)
    MoveR(0, 20)
    LeftClick(50, 120)
    # time.sleep(3)
    print("年龄输入成功，人为延时")


def input_patient_sex(sex: str):
    if sex == "男":
        # 性别位置
        # 男
        # MoveTo(1920 // 2 + 96, 316)  # 有身高体重那套的
        MoveTo(1920 // 2 + 96, 280)
        LeftClick(50, 120)

    else:
        # # 女
        # MoveTo(1920 // 2 + 148, 316)  # 有身高体重那套的
        MoveTo(1920 // 2 + 150, 280)
        LeftClick(50, 120)
    print("性别输入成功，人为延时")
    # time.sleep(3)


def patient_chest_button_low():
    # 人体胸部按钮 + 胸部平扫 位置
    MoveTo(1920 // 2 + 320, 390)
    # time.sleep(1.5)
    # MoveTo(1920//2+320, 399)
    time.sleep(0.5)
    LeftClick(50, 120)
    time.sleep(0.5)
    # MoveR(20, 23)
    MoveR(20, 79)
    time.sleep(0.5)
    LeftClick(50, 120)
    print("人体胸部按钮 + 胸部平扫 位置选择成功，人为延时")


def patient_chest_button_high():
    # 人体胸部按钮 + 胸部平扫 位置
    MoveTo(1920 // 2 + 320, 390)
    # time.sleep(1.5)
    # MoveTo(1920//2+320, 399)
    time.sleep(0.5)
    LeftClick(50, 120)
    time.sleep(0.5)
    # MoveR(20, 23)
    MoveR(20, 23)
    time.sleep(0.5)
    LeftClick(50, 120)
    print("人体胸部按钮 + 胸部平扫 位置选择成功，人为延时")


def patient_head_button():
    # 人体胸部按钮 + 胸部平扫 位置
    MoveTo(1920 // 2 + 540, 280)
    # time.sleep(1.5)
    # MoveTo(1920//2+320, 399)
    time.sleep(0.5)
    LeftClick(50, 120)
    time.sleep(0.5)
    MoveR(20, 29)
    time.sleep(0.5)
    LeftClick(50, 120)
    print("人体胸部按钮 + 胸部平扫 位置选择成功，人为延时")


def patient_check():
    # 点击 患者检查 绿色按钮
    MoveTo(1920 // 2 + 300, 1080 - 70)
    LeftClick(50, 120)


def close_eye_button():
    # # 关闭天眼
    MoveTo(1920 - 230, 90)
    LeftClick(50, 120)


def yes_button_1():
    # 移动调整扫描床后，的确认按钮
    # TODO 定位片吧？？
    MoveTo(1920 - 200, 1080 - 60)
    LeftClick(50, 120)


def adjust_top_bottom_line():
    # # 可调节的断层的框的上线的位置
    MoveTo(1920 // 2 + 100, 310)
    LeftDown()
    MoveR(0, -10)
    LeftUp()

    # 可调节的断层的框的下线的位置
    MoveTo(1920 // 2 + 100, 685)
    LeftDown()
    MoveR(0, 10)
    LeftUp()


def yes_button2():
    # 正片扫描完成后的完成按钮
    MoveTo(1920 - 50, 1080 - 60)
    print("请查看鼠标位置是否正确")
    # time.sleep(5)
    LeftClick(50, 120)


def input_inbed_positon(input_position):
    # MoveTo(1920 - 130, 1080 - 467+25)
    # LeftClick(50, 120)
    # time.sleep(1)
    MoveTo(1920 - 130, 1080 - 467)
    LeftClick(50, 120)
    KeyDown("Ctrl")
    KeyPress("A", 20, 40)
    KeyUp("Ctrl")
    KeyPress("BackSpace", 20, 40)
    print("下面是输入的进床距离")
    print(str(input_position))
    SayString(str(input_position), 20, 40)
    # SayString(str(input_position), 200, 400)
    time.sleep(1)
    KeyPress("Enter", 20, 40)
    # print("入床位置输入完成")
    # print("点击确认按钮")
    # time.sleep(1)
    # MoveTo(1920 - 180, 1080- 70)
    # LeftClick(50, 120)


def input_inbed_positon_have_button():
    # MoveTo(1920 - 130, 1080 - 467+25)
    # LeftClick(50, 120)
    # time.sleep(1)
    # MoveTo(1920 - 130, 1080- 467)
    # LeftClick(50, 120)
    # KeyDown("Ctrl")
    # KeyPress("A", 20, 40)
    # KeyUp("Ctrl")
    # KeyPress("BackSpace", 20, 40)
    # print("下面是输入的进床距离")
    # print(str(input_position))
    # SayString(str(input_position), 20, 40)
    # # SayString(str(input_position), 200, 400)
    # time.sleep(1)
    # KeyPress("Enter", 20, 40)
    # print("入床位置输入完成")
    # print("点击确认按钮")
    # time.sleep(1)
    MoveTo(1920 - 180, 1080 - 70)
    LeftClick(50, 120)



def input_patient_hight(hight: str):
    # 身高位置
    MoveTo(1920 // 2 + 100, 280)
    LeftClick(50, 120)
    SayString(hight, 20, 40)
    print("身高输入成功，人为延时")


def input_patient_weight(weight: str):
    # 体重位置
    MoveTo(1920 // 2 + 220, 280)
    LeftClick(50, 120)
    SayString(weight, 20, 40)
    print("体重输入成功，人为延时")


# 关闭天眼
def shut_down_skyeyes():
    MoveTo(1920 // 2 + 730, 95)
    LeftClick(50, 120)


def pull_locator(up: int, up_bound: int, down: int, down_bound: int):
    # TODO 图片尺寸和屏幕尺寸的对应

    # move 上的线位置
    # TODO 假设是移动到屏幕弹出框的上边界
    MoveTo(1920 // 2 + 220, up)
    LeftDown()
    time.sleep(3)
    # move upbound的位置
    MoveTo(1920 // 2 + 220, up_bound)
    LeftUp()

    time.sleep(1)
    # TODO 假设现在moveto到了下边界
    MoveTo(1920 // 2 + 220, down)
    LeftDown()
    # move upbound的位置
    MoveTo(1920 // 2 + 220, down_bound)
    LeftUp()


def pull_locator_fixed(up_bound: int, down_bound: int):
    # 上边框
    MoveTo(1920 // 2 + 200, 312)
    LeftDown()
    time.sleep(1)
    # move upbound的位置
    MoveTo(1920 // 2 + 200, up_bound)
    LeftUp()
    time.sleep(2)
    # 下边框
    MoveTo(1920 // 2 + 200, 684)
    LeftDown()
    time.sleep(1)
    # move upbound的位置
    MoveTo(1920 // 2 + 200, down_bound)
    LeftUp()


def pull_locator_fixed_right(right_bound: int):
    # 固定的左右边框位置
    # 右边框
    MoveTo(1920 // 2 + 312, 600)
    LeftDown()
    time.sleep(1)
    MoveTo(1920 // 2 + right_bound, 600)
    LeftUp()


def pull_locator_fixed_left(left_bound: int):
    # 左边框
    MoveTo(1920 // 2 + 68, 600)
    LeftDown()
    time.sleep(1)
    MoveTo(1920 // 2 + left_bound, 600)
    LeftUp()


def pull_locator_fixed_middle(middle_bound: int):
    # 左边框
    MoveTo(1920 // 2 + 188, 600)
    LeftDown()
    time.sleep(0.5)
    MoveTo(1920 // 2 + middle_bound, 600)
    LeftUp()

def pull_point(data):
    MoveTo(1920 // 2 + 850, 635)
    LeftClick(50, 120)
    # data=str(400)
    SayString(data, 20, 40)
    time.sleep(1)
    KeyPress("Enter", 20, 40)
if __name__ == '__main__':
    # pull_locator_fixed_middle(60)
    pull_point()
    pass
    # input_inbed_positon(data)
    # {"id": "H70468468", "name": "GUO HAI FENG", "age": "69", "sex": "男"}
    # id='H70468468'
    # name="GUO HAI FENG"
    # name = "gui HAI FENG"
    # input_patient_id(id)
    # input_patient_name(name)
    # yes_button_1()
    # MoveTo(  200, 312)
    # time.sleep(1)
    # MoveTo(200, 282)
    # MoveTo(1920 // 2 + 200, 312)
    # time.sleep(1)
    #
    # MoveTo(1920 // 2 + 200, 312-30)
    # time.sleep(2)
    # # 下边框
    # MoveTo(1920 // 2 + 200, 684)
    # time.sleep(1)
    # MoveTo(1920 // 2 + 200, 684+150)
    # input_inbed_positon(-320)
    # pass
    # patient_head_button()
    # click_middle_error_button()
    # MoveTo(1920 // 2 + 200, 312)
    # # LeftDown()
    # time.sleep(1)
    # # move upbound的位置
    # # MoveTo(1920 // 2 + 200,up_bound)
    # MoveTo(1920 // 2 + 200, 312-30)
    # time.sleep(1)
    # # LeftUp()
    # MoveTo(1920 // 2 + 200, 312)
    # time.sleep(2)
    #
    # # 右边框
    # MoveTo(1920 // 2 + 312, 600)
    # LeftDown()
    # time.sleep(1)
    # move upbound的位置
    # MoveTo(1920 // 2 + 200,down_bound)
    # MoveTo(1920 // 2 + 200, 684+100)
    # LeftUp()
    # time.sleep(1)
    # MoveTo(1920 //2 +64+1, 600)
    # MoveTo(961+64, 400)
    # time.sleep(1)
    # MoveTo(1920 //2 +64+1, 600)
    # MoveTo(961+64+1, 400)
    # pull_locator_fixed_right_left(10,10)
    # MoveTo(1920 //2 +80, 600)
    # # LeftDown()
    # time.sleep(1)
    # LeftDown()
    # time.sleep(1)
    # # move upbound的位置
    # MoveTo(1920 // 2 + 69,600)
    # # MoveTo(1920 // 2 + 200, 684+100)
    # LeftUp()
    # time.sleep(1)
    # MoveTo(1920 //2 +64+1, 600)
    # LeftDown()
    # time.sleep(1)
    # MoveTo(1920 // 2 +right_bound, 600)

    # MoveTo(1920 // 2 + 312, 600)
    # MoveTo(1920 // 2 + 64, 600)
    # MoveTo(1920 // 2 + 68, 600)
    # LeftDown()
    # time.sleep(1)
    # MoveTo(1920 // 2 +left_bound, 600)
    # LeftUp()
    # time.sleep(2)
    # 右边框
    # MoveTo(1920 //2 +64+50, 600)
    # LeftDown()
    # time.sleep(1)
    # MoveTo(1920 // 2 +right_bound, 600)
    # LeftUp()
    # patient_chest_button_low()
    # patient_chest_button_high()

