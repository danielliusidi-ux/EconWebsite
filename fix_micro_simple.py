#!/usr/bin/env python3
"""
简单修复AP Micro题目选项E中的问题
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

# 提取QUESTION_BANK
question_bank_start = content.find("QUESTION_BANK = {")
list_start = content.find('{', question_bank_start)
list_end = find_matching_bracket(content, list_start)
list_str = content[list_start:list_end+1]

question_bank = ast.literal_eval(list_str)
questions = question_bank['ap_micro']
print(f"找到 {len(questions)} 道AP Micro题目\n")

# 定义需要修复的题目ID
problem_ids = [42, 54, 56, 84, 95, 125, 129, 155, 174, 187, 276, 316, 337, 354, 366, 439]

# 修复所有有问题的题目
fixed_count = 0
for q in questions:
    q_id = q.get('id')
    if q_id in problem_ids:
        print(f"正在修复题目 {q_id}")
        options = q.get('options', [])
        
        if len(options) > 4:
            opt_e = options[4]
            original_opt = opt_e
            
            # 找到需要截断的位置
            cut_index = len(opt_e)
            
            # 检查'Refer'
            if 'Refer' in opt_e:
                refer_idx = opt_e.find('Refer')
                if refer_idx < cut_index:
                    cut_index = refer_idx
            
            # 检查'CHAPTER'
            if 'CHAPTER' in opt_e:
                chapter_idx = opt_e.find('CHAPTER')
                if chapter_idx < cut_index:
                    cut_index = chapter_idx
            
            # 检查'Chapter'（小写c）
            if 'Chapter' in opt_e:
                chapter_idx = opt_e.find('Chapter')
                if chapter_idx < cut_index:
                    cut_index = chapter_idx
            
            # 截断并去除末尾空格
            if cut_index < len(opt_e):
                new_opt_e = opt_e[:cut_index].strip()
                options[4] = new_opt_e
                print(f"  原选项: {original_opt}")
                print(f"  新选项: {new_opt_e}")
                print()
                fixed_count += 1

# 更新question_bank
question_bank['ap_micro'] = questions

# 更新app.py
new_list_str = repr(question_bank)
new_content = content[:list_start] + new_list_str + content[list_end+1:]

with open('/Users/bytedance/Desktop/SideProject/EconWebsite/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n更新完成！共修复了 {fixed_count} 道AP Micro题目。")
