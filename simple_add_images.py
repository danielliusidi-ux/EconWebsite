#!/usr/bin/env python3
import os
import re

# 读取app.py文件
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查图片目录
image_dir = 'static/images/micro'
if not os.path.exists(image_dir):
    print(f"ERROR: Image directory {image_dir} not found")
    exit(1)

# 获取所有图片文件
image_files = os.listdir(image_dir)
micro_images = [f for f in image_files if f.startswith('micro_q') and f.endswith('.png')]

print(f"Found {len(micro_images)} micro images")

# 构建图片映射字典
image_map = {}
for img in micro_images:
    try:
        # 从文件名提取题目ID
        q_id = int(img.replace('micro_q', '').replace('.png', ''))
        image_map[q_id] = f"images/micro/{img}"
    except:
        pass

print(f"Mapped {len(image_map)} images to question IDs")

# 处理每个题目ID
updated_content = content
for q_id, image_path in image_map.items():
    # 查找包含该ID的题目
    pattern = fr"('id':*{q_id},)(?!.*'image':)"
    replacement = fr"'id': {q_id}, 'image': '{image_path}',"
    
    # 使用正则表达式替换
    updated_content = re.sub(pattern, replacement, updated_content)
    print(f"Processing question {q_id}")

# 写回文件
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("\n=== Process completed ===")
print("Images have been added to AP Micro questions where applicable")
