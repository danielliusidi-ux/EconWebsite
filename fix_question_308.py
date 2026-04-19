#!/usr/bin/env python3
"""
修改AP Macro第308题的选项E，把Refer以及后面的语句都删掉
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
print(f"找到 {len(questions)} 道题目")

# 找到第308题并修改
for q in questions:
    if q.get('id') == 308:
        print("找到第308题！")
        options = q.get('options', [])
        print(f"原选项:")
        for i, opt in enumerate(options):
            print(f"  {opt}")
        
        # 修改选项E，删除"Refer"以及后面的语句
        if len(options) > 4:
            opt_e = options[4]
            if 'Refer' in opt_e:
                # 找到'Refer'的位置，然后保留到这个位置之前
                refer_index = opt_e.find('Refer')
                if refer_index != -1:
                    new_opt_e = opt_e[:refer_index].strip()
                    options[4] = new_opt_e
        
        q['options'] = options
        print(f"\n新选项:")
        for i, opt in enumerate(options):
            print(f"  {opt}")
        break

# 更新app.py
new_list_str = repr(questions)
new_content = content[:list_start] + new_list_str + content[list_end+1:]

with open('/Users/bytedance/Desktop/SideProject/EconWebsite/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n更新完成！第308题已修改。")
