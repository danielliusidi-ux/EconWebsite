#!/usr/bin/env python3
"""
修复AP Micro中还保留其他无关内容的题目
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
micro_list_start = content.find('[', ap_micro_start)
micro_list_end = find_matching_bracket(content, micro_list_start)
micro_list_str = content[micro_list_start:micro_list_end+1]
micro_questions = ast.literal_eval(micro_list_str)

# 提取ap_macro列表
ap_macro_start = content.find("'ap_macro':")
macro_list_start = content.find('[', ap_macro_start)
macro_list_end = find_matching_bracket(content, macro_list_start)
macro_list_str = content[macro_list_start:macro_list_end+1]
macro_questions = ast.literal_eval(macro_list_str)

# 定义需要进一步修复的题目和它们的正确选项E
additional_fix_map = {
    54: "(E) The curve would shift to the right and become concave.",
    56: "(E) 300 cookies",
    125: "(E) luxury goods",
    337: "(E) leave the oil price and quantity supplied unchanged"
}

# 修复
fixed_count = 0
for q_id, correct_opt_e in additional_fix_map.items():
    for q in micro_questions:
        if q.get('id') == q_id:
            options = q.get('options', [])
            if len(options) > 4:
                opt_e = options[4]
                if opt_e != correct_opt_e:
                    print(f"正在修复题目 {q_id}")
                    print(f"  原选项: {opt_e}")
                    print(f"  新选项: {correct_opt_e}")
                    options[4] = correct_opt_e
                    fixed_count += 1

# 重新生成QUESTION_BANK
qb_start = content.find('QUESTION_BANK = {')
new_content = content[:qb_start] + 'QUESTION_BANK = {\n'
new_content += "    'ap_micro': " + repr(micro_questions) + ",\n"
new_content += "    'ap_macro': " + repr(macro_questions) + "\n"
new_content += '}'

# 找到QUESTION_BANK结束位置
qb_end = -1
bracket_count = 0
in_string = False
string_char = None
escape_next = False

for i in range(qb_start, len(content)):
    char = content[i]
    
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
        if char == '{':
            bracket_count += 1
        elif char == '}':
            bracket_count -= 1
            if bracket_count == 0:
                qb_end = i
                break

if qb_end != -1:
    new_content += content[qb_end+1:]

# 写入文件
with open('/Users/bytedance/Desktop/SideProject/EconWebsite/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n更新完成！共修复了 {fixed_count} 道AP Micro题目。")
