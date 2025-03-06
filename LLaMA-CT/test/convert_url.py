import json

def update_image_urls(file_path):
    # 读取原始JSON文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 定义URL前缀
    prefix = "https://llm-1323287448.cos.ap-beijing.myqcloud.com/"
    
    # 更新每个条目中的图片URL
    for item in data:
        if "images" in item:
            item["images"] = [prefix + img_path for img_path in item["images"]]
    
    # 保存更新后的JSON文件
    output_path = file_path.replace('.json', '_updated.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已更新图片URL并保存至: {output_path}")

if __name__ == "__main__":
    file_path = "/root/autodl-tmp/2-15test/llama-ct-test_data.json"
    update_image_urls(file_path)