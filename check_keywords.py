#!/usr/bin/env python3
"""
检查关键词搜索结果
"""

import ast

# 读取app.py
with open('/Users/bytedance/Desktop/SideProject/EconWebsite/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

def find_matching_bracket(text, start):
    bracket_count = 0
    in_string = False
    string_char = None
    escape_next = False

    for i in range(start, len(text)):
        char = text[i]

        if escape_next:
            escape_next = False
            continue

        if char == '\\':
            escape_next = True
            continue

        if char in ('"', "'"):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
            continue

        if not in_string:
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    return i

    return -1

# 提取ap_macro列表
ap_macro_start = content.find("'ap_macro':")
list_start = content.find('[', ap_macro_start)
list_end = find_matching_bracket(content, list_start)
list_str = content[list_start:list_end+1]
questions = ast.literal_eval(list_str)

print(f"总共有 {len(questions)} 道AP Macro题目\n")

# 检查包含"CPI"或"consumer price index"的题目
cpi_matches = []
cpi_text_matches = []

for q in questions:
    text = ' '.join([
        q.get('question', ''),
        ' '.join(q.get('options', [])),
        q.get('explanation', '')
    ]).lower()
    
    if 'cpi' in text:
        cpi_matches.append(q)
    if 'consumer price index' in text:
        cpi_text_matches.append(q)

print(f"包含 'CPI' 的题目: {len(cpi_matches)} 道")
for q in cpi_matches:
    print(f"  ID: {q['id']} - {q['question'][:50]}...")

print(f"\n包含 'consumer price index' 的题目: {len(cpi_text_matches)} 道")
for q in cpi_text_matches:
    print(f"  ID: {q['id']} - {q['question'][:50]}...")

print(f"\n两者合起来共有 {len(set([q['id'] for q in cpi_matches + cpi_text_matches]))} 道不同的题目")
