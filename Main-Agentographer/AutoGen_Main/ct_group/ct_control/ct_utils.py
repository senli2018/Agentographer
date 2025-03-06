import time
import cv2
import numpy as np
import requests
def retry_request(session, url, params, retries=3):
    """
    发送请求，并通过重试机制确保请求尽可能成功。
    :param session: requests.Session 对象
    :param url: 请求的 URL
    :param params: 请求参数
    :param retries: 最大重试次数
    :return: 响应对象
    :raises: 如果超过重试次数仍失败，则抛出异常
    """
    for attempt in range(retries):
        try:
            response = session.get(url, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt + 1 == retries:
                raise
            time.sleep(1)
def pcb_up(t: float):
    """控制床升起来

        Args:
            t(float): 按下时间
    """
    import requests
    session = requests.Session()

    baseurl = 'http://192.168.1.200:80/mb'
    params1 = {'opr': 'open', 'io':  1, 'addr': 254}
    params2 = {'opr': 'open', 'io':  2, 'addr': 254}

    params3 = {'opr': 'close', 'io': 1, 'addr': 254}
    params4 = {'opr': 'close', 'io': 2, 'addr': 254}

    response1 = retry_request(session, baseurl, params1)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)

    response2 = retry_request(session, baseurl, params2)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)

    time.sleep(t)

    response3 = retry_request(session, baseurl, params3)
    response3.raise_for_status()
    print("First request succeeded:", response1.text)

    response4 = retry_request(session, baseurl, params4)
    response4.raise_for_status()
    print("Second request succeeded:", response2.text)
def pcb_one_click():
    """控制床一键移床，
    """
    import requests
    session = requests.Session()
    baseurl = 'http://192.168.1.200:80/mb'
    params1 = {'opr': 'open', 'io':  15, 'addr': 254}
    params2 = {'opr': 'open', 'io':  16, 'addr': 254}
    params3 = {'opr': 'close', 'io': 15, 'addr': 254}
    params4 = {'opr': 'close', 'io': 16, 'addr': 254}
    response1 = retry_request(session, baseurl, params1)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = retry_request(session, baseurl, params2)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    time.sleep(1)
    response1 = retry_request(session, baseurl, params3)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = retry_request(session, baseurl, params4)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
def pcb_quit_bed():
    """控制床一键退床
    """
    import requests
    session = requests.Session()
    baseurl = 'http://192.168.1.200:80/mb'
    params1 = {'opr': 'open', 'io':  9, 'addr': 254}
    params2 = {'opr': 'open', 'io':  10, 'addr': 254}
    params3 = {'opr': 'close', 'io': 9, 'addr': 254}
    params4 = {'opr': 'close', 'io': 10, 'addr': 254}
    response1 = retry_request(session, baseurl, params1)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = retry_request(session, baseurl, params2)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    time.sleep(18)
    response1 = retry_request(session, baseurl, params3)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = retry_request(session, baseurl, params4)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
def pcb_scan():
    """控制床扫描
    """
    import requests
    session = requests.Session()
    baseurl = 'http://192.168.1.200:80/mb'
    params1 = {'opr': 'open', 'io':  11, 'addr': 254}
    params2 = {'opr': 'open', 'io':  12, 'addr': 254}
    params3 = {'opr': 'close', 'io': 11, 'addr': 254}
    params4 = {'opr': 'close', 'io': 12, 'addr': 254}
    response1 = retry_request(session, baseurl, params1)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = retry_request(session, baseurl, params2)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    time.sleep(1)
    response1 = session.get(baseurl, params=params3)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = session.get(baseurl, params=params4)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
def button_close_all():
    """关闭开关
    """
    import requests
    session = requests.Session()
    baseurl = 'http://192.168.1.200:80/mb'
    params1 = {'opr': 'close', 'io': 1, 'addr': 254}
    params2 = {'opr': 'close', 'io': 2, 'addr': 254}
    params3 = {'opr': 'close', 'io': 9, 'addr': 254}
    params4 = {'opr': 'close', 'io': 10, 'addr': 254}
    params5 = {'opr': 'close', 'io': 11, 'addr': 254}
    params6 = {'opr': 'close', 'io': 12, 'addr': 254}
    params7 = {'opr': 'close', 'io': 15, 'addr': 254}
    params8 = {'opr': 'close', 'io': 16, 'addr': 254}
    response1 = session.get(baseurl, params=params1)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = session.get(baseurl, params=params2)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    response1 = session.get(baseurl, params=params3)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = session.get(baseurl, params=params4)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    response1 = session.get(baseurl, params=params5)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = session.get(baseurl, params=params6)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    response1 = session.get(baseurl, params=params7)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = session.get(baseurl, params=params8)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    return "已确保所有关闭关闭"
def button_close_all_system_check():
    """关闭开关
    """
    import requests
    session = requests.Session()
    baseurl = 'http://192.168.1.200:80/mb'
    params1 = {'opr': 'close', 'io': 1, 'addr': 254}
    params2 = {'opr': 'close', 'io': 2, 'addr': 254}
    params3 = {'opr': 'close', 'io': 9, 'addr': 254}
    params4 = {'opr': 'close', 'io': 10, 'addr': 254}
    params5 = {'opr': 'close', 'io': 11, 'addr': 254}
    params6 = {'opr': 'close', 'io': 12, 'addr': 254}
    params7 = {'opr': 'close', 'io': 15, 'addr': 254}
    params8 = {'opr': 'close', 'io': 16, 'addr': 254}
    response1 = session.get(baseurl, params=params1)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = session.get(baseurl, params=params2)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    response1 = session.get(baseurl, params=params3)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = session.get(baseurl, params=params4)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    response1 = session.get(baseurl, params=params5)
    response1.raise_for_status()
    print("First request succeeded:", response1.text)
    response2 = session.get(baseurl, params=params6)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    response2 = session.get(baseurl, params=params8)
    response2.raise_for_status()
    print("Second request succeeded:", response2.text)
    return "已确保所有关闭关闭"

if __name__ == "__main__":
    pass
    pcb_scan()




