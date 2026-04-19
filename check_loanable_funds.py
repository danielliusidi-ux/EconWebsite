#!/usr/bin/env python3
"""
检查'loanable funds'相关题目
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

print(f"AP Macro总共有 {len(questions)} 道题目\n")

# 先检查ID: 414
print("检查题目ID: 414")
for q in questions:
    if q.get('id') == 414:
        print("题目:", q.get('question', ''))
        print("\n选项:")
        for opt in q.get('options', []):
            print("  ", opt)
        print("\n解释:", q.get('explanation', ''))
        print()
        break

print("\n" + "="*80 + "\n")

# 搜索包含'loanable'或'funds'的题目
print("搜索包含'loanable'或'funds'的题目:")
for q in questions:
    text = ' '.join([
        q.get('question', ''),
        ' '.join(q.get('options', [])),
        q.get('explanation', '')
    ]).lower()
    
    if 'loanable' in text or 'funds' in text:
        print(f"\n题目ID: {q['id']}")
        print(f"题目: {q['question'][:80]}...")
        print(f"包含'loanable': {'loanable' in text}")
        print(f"包含'funds': {'funds' in text}")
