#!/usr/bin/env python3
import os
import json

# 读取app.py文件
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取QUESTION_BANK部分
import re
pattern = r'QUESTION_BANK = \{([\s\S]*?)\}'
match = re.search(pattern, content)
if not match:
    print("ERROR: QUESTION_BANK not found in app.py")
    exit(1)

question_bank_str = match.group(0)

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

# 处理QUESTION_BANK字符串
def add_images_to_questions(qbank_str, image_map):
    # 简单的字符串替换方法
    lines = qbank_str.split('\n')
    updated_lines = []
    
    in_ap_micro = False
    for line in lines:
        # 检查是否进入ap_micro部分
        if "'ap_micro': [" in line:
            in_ap_micro = True
        elif "'ap_macro': [" in line:
            in_ap_micro = False
        
        # 只有在ap_micro部分且包含id字段时才处理
        if in_ap_micro and '"id":' in line:
            # 提取题目ID
            id_match = re.search(r'"id"\s*:\s*(\d+)', line)
            if id_match:
                q_id = int(id_match.group(1))
                # 检查是否有对应图片
                if q_id in image_map:
                    # 在下一行添加image字段
                    image_path = image_map[q_id]
                    indent = line[:line.index('"id"')]
                    image_line = f'{indent}"image": "{image_path}",'
                    updated_lines.append(line)
                    updated_lines.append(image_line)
                    print(f"Added image for question {q_id}")
                    continue
        
        updated_lines.append(line)
    
    return '\n'.join(updated_lines)

# 处理题目库
updated_question_bank = add_images_to_questions(question_bank_str, image_map)

# 替换原文件中的QUESTION_BANK
updated_content = content.replace(question_bank_str, updated_question_bank)

# 写回文件
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("\n=== Process completed ===")
print("Images have been added to AP Micro questions where applicable")
