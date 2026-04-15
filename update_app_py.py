#!/usr/bin/env python3
"""
更新app.py中的QUESTION_BANK
"""

import re

# 读取parsed_questions.py
with open('parsed_questions.py', 'r', encoding='utf-8') as f:
    parsed_content = f.read()

# 读取app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# 提取ap_micro和ap_macro数据（只提取列表内容）
ap_micro_match = re.search(r'ap_micro = (\[.*?\])(?=\n\n|\Z)', parsed_content, re.DOTALL)
ap_macro_match = re.search(r'ap_macro = (\[.*?\])(?=\n\n|\Z)', parsed_content, re.DOTALL)

if not ap_micro_match or not ap_macro_match:
    print("错误: 无法从parsed_questions.py中提取题目数据")
    exit(1)

ap_micro_list = ap_micro_match.group(1)
ap_macro_list = ap_macro_match.group(1)

# 构建新的QUESTION_BANK
new_question_bank = f"""QUESTION_BANK = {{
    'ap_micro': {ap_micro_list},
    'ap_macro': {ap_macro_list}
}}"""

# 找到QUESTION_BANK并替换整个内容
start_marker = "QUESTION_BANK = {"
start_idx = app_content.find(start_marker)
if start_idx == -1:
    print("错误: 无法找到QUESTION_BANK")
    exit(1)

# 找到匹配的结束括号
brace_count = 0
end_idx = start_idx
for i, char in enumerate(app_content[start_idx:]):
    if char == '{':
        brace_count += 1
    elif char == '}':
        brace_count -= 1
        if brace_count == 0:
            end_idx = start_idx + i + 1
            break

# 替换
updated_content = app_content[:start_idx] + new_question_bank + app_content[end_idx:]

# 保存更新后的app.py
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("成功更新app.py中的QUESTION_BANK")
ap_micro_count = ap_micro_list.count("'id':")
ap_macro_count = ap_macro_list.count("'id':")
print(f"ap_micro: {ap_micro_count} 道题目")
print(f"ap_macro: {ap_macro_count} 道题目")
