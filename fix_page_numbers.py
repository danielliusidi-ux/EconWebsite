#!/usr/bin/env python3
"""
修复AP Macro题目选项E中的页码数字
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
print(f"找到 {len(questions)} 道题目\n")

# 定义需要进一步修复的题目ID和它们的页码
page_number_ids = {
    70: ' 40',
    170: ' 67', 
    315: ' 109',
    412: ' 135',
    440: ' 144'
}

# 修复页码数字
fixed_count = 0
for q in questions:
    q_id = q.get('id')
    if q_id in page_number_ids:
        print(f"正在修复题目 {q_id}")
        options = q.get('options', [])
        
        if len(options) > 4:
            opt_e = options[4]
            original_opt = opt_e
            page_num = page_number_ids[q_id]
            
            if page_num in opt_e:
                new_opt_e = opt_e.replace(page_num, '').strip()
                options[4] = new_opt_e
                print(f"  原选项: {original_opt}")
                print(f"  新选项: {new_opt_e}")
                print()
                fixed_count += 1

# 更新app.py
new_list_str = repr(questions)
new_content = content[:list_start] + new_list_str + content[list_end+1:]

with open('/Users/bytedance/Desktop/SideProject/EconWebsite/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n更新完成！共修复了 {fixed_count} 道题目。")
