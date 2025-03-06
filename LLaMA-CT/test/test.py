import json
import requests
import time
import base64
from pathlib import Path

LLAMA_API_URL = "http://localhost:8000/v1/chat/completions"  
TEST_DATA_PATH = "/root/autodl-tmp/SourceCode/test/llama-ct-test_data_updated.json"  
RESULT_PATH = "/root/autodl-tmp/SourceCode/test/test_results1.json"  

def load_test_data(file_path):
    """加载测试数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def call_llama_api(messages, image_path, max_retries=3, retry_delay=5):
    """调用Llama API
    Args:
        messages: 消息历史列表
        image_path: 图片路径
        max_retries: 最大重试次数
        retry_delay: 重试间隔（秒）
    """
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

def compare_and_save_results(test_data):
    """比较结果并保存"""
    results = []
    
    for item in test_data:
        image_path = item['images'][0]
        qa_pairs = []
        current_messages = []
        
        for i in range(0, len(item['messages']), 2):
            if i + 1 >= len(item['messages']):
                break
                
            question = item['messages'][i]
            original_answer = item['messages'][i + 1]
            
            # 更新消息历史
            current_messages.append(question)
            
            # 调用API获取回答
            model_answer = call_llama_api(current_messages, image_path)
            
            # 保存问答对
            qa_pairs.append({
                'question': question['content'],
                'original_answer': original_answer['content'],
                'model_answer': model_answer
            })
            
            # 将原始答案添加到消息历史
            current_messages.append(original_answer)
        
        results.append({
            'image': image_path,
            'qa_pairs': qa_pairs
        })
    
    # 保存结果
    with open(RESULT_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results

def main():
    # 加载测试数据
    test_data = load_test_data(TEST_DATA_PATH)
    
    # 执行测试并保存结果
    results = compare_and_save_results(test_data)
    
    # 打印测试统计信息
    total_questions = sum(len(item['qa_pairs']) for item in results)
    
    print(f"\n测试完成!")
    print(f"总问题数: {total_questions}")
    print(f"\n详细结果已保存到: {RESULT_PATH}")

if __name__ == "__main__":
    main()