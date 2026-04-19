#!/usr/bin/env python3
import os
import re
import ast

# 读取app.py文件
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取QUESTION_BANK部分
pattern = r'QUESTION_BANK = \{([\s\S]*?)\}'
match = re.search(pattern, content)
if not match:
    print("ERROR: QUESTION_BANK not found in app.py")
    exit(1)

question_bank_str = match.group(0)

# 解析QUESTION_BANK为Python对象
try:
    # 提取字典部分
    dict_str = question_bank_str.replace('QUESTION_BANK = ', '')
    question_bank = ast.literal_eval(dict_str)
    print("Successfully parsed QUESTION_BANK")
except Exception as e:
    print(f"ERROR: Failed to parse QUESTION_BANK: {e}")
    exit(1)

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

# 为AP Micro题目添加图片
if 'ap_micro' in question_bank:
    micro_questions = question_bank['ap_micro']
    added_count = 0
    
    for q in micro_questions:
        q_id = q.get('id')
        if q_id in image_map and 'image' not in q:
            q['image'] = image_map[q_id]
            added_count += 1
            print(f"Added image for question {q_id}")
    
    print(f"Added images to {added_count} AP Micro questions")

# 生成更新后的QUESTION_BANK字符串
updated_qbank_str = f"QUESTION_BANK = {question_bank}"

# 替换原文件中的QUESTION_BANK
updated_content = content.replace(question_bank_str, updated_qbank_str)

# 写回文件
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("\n=== Process completed ===")
print("Images have been added to AP Micro questions where applicable")
