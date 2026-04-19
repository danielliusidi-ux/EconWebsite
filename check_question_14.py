#!/usr/bin/env python3
"""
检查ID:14这道题的内容
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

# 提取ap_micro列表
ap_micro_start = content.find("'ap_micro':")
list_start = content.find('[', ap_micro_start)
list_end = find_matching_bracket(content, list_start)
list_str = content[list_start:list_end+1]
questions = ast.literal_eval(list_str)

# 找ID: 14的题
for q in questions:
    if q.get('id') == 14:
        print("题目ID: 14")
        print("题目:", q.get('question', ''))
        print("\n选项:")
        for opt in q.get('options', []):
            print("  ", opt)
        print("\n解释:", q.get('explanation', ''))
        print("\n完整文本:")
        full_text = ' '.join([
            q.get('question', ''),
            ' '.join(q.get('options', [])),
            q.get('explanation', '')
        ]).lower()
        print(full_text)
        print("\n'perfect' in text?", 'perfect' in full_text)
        print("'competition' in text?", 'competition' in full_text)
        break
