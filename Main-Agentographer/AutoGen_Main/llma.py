import requests
import json
import time
LLAMA_API_URL = ""  # 替换为你的API地址
def call_llama_api(messages, max_retries=3, retry_delay=5):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    for attempt in range(max_retries):
        try:
            # 构建请求数据
            payload = {
                "model": "llama-2-13b-chat",
                "messages": [],
                "stream": False,
                "max_tokens": 1024,
                "temperature": 0.7
            }
            # 处理消息和图片
            for msg in messages:
                if msg.get("content"):
                    if msg.get("role") == "user" and "<image>" in msg["content"]:
                        payload["messages"].append({
                            "role": msg.get("role", "user"),
                            "content": [
                                {
                                    "type": "text",
                                    "text": msg["content"].replace("<image>", "").strip()
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_path
                                    }
                                }
                            ]
                        })
                    else:
                        payload["messages"].append({
                            "role": msg.get("role", "user"),
                            "content": msg["content"].strip()
                        })

            # 打印请求信息（调试用）
            print(f"\n发送请求到: {LLAMA_API_URL}")
            print(f"请求数据: {json.dumps(payload, ensure_ascii=False, indent=2)}")

            # 发送请求
            response = requests.post(LLAMA_API_URL, json=payload, headers=headers, timeout=30)

            # 检查响应状态
            if response.status_code != 200:
                print(f"API响应错误 - 状态码: {response.status_code}")
                print(f"错误详情: {response.text}")
                if attempt < max_retries - 1:
                    print(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    continue
                return None

            # 解析响应数据
            response_data = response.json()
            if not response_data.get("choices"):
                print("API响应格式错误: 未找到'choices'字段")
                return None

            return response_data['choices'][0]['message']['content']

        except FileNotFoundError as e:
            print(f"文件错误: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {str(e)}")
            print(f"原始响应: {response.text}")
            if attempt < max_retries - 1:
                print(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                continue
            return None
        except requests.RequestException as e:
            print(f"请求错误: {str(e)}")
            if attempt < max_retries - 1:
                print(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                continue
            return None
        except Exception as e:
            print(f"未知错误: {str(e)}")
            return None

    return None

if __name__ == "__main__":
    image_path = r""
    messages = [
        {"role": "user",
         "content": "大门是开的还是关闭的，请用0和1来回复，1代表开着，0代表关着"}
    ]
    data=call_llama_api(messages, image_path)
    print(data)
