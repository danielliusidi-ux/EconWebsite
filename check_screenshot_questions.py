#!/usr/bin/env python3
"""
检查用户截图中的题目
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

# 检查题目ID 6, 7, 8
for q_id in [6, 7, 8]:
    for q in questions:
        if q.get('id') == q_id:
            print(f"{'='*80}")
            print(f"题目ID: {q_id}")
            print(f"题目: {q.get('question', '')}")
            print(f"\n选项:")
            for opt in q.get('options', []):
                print(f"  {opt}")
            print(f"\n解释: {q.get('explanation', '')}")
            
            full_text = ' '.join([
                q.get('question', ''),
                ' '.join(q.get('options', [])),
                q.get('explanation', '')
            ]).lower()
            
            print(f"\n'perfect' in text? {'perfect' in full_text}")
            print(f"'competition' in text? {'competition' in full_text}")
            break
