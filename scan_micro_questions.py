#!/usr/bin/env python3
"""
扫描所有AP Micro题目，找出选项E中包含无关内容的题目
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
print(f"找到 {len(questions)} 道AP Micro题目\n")

# 定义需要检查的关键词
problem_keywords = [
    'Refer',
    'CHAPTER',
    'Chapter',
    'Refer to the following',
    'Refer to the',
]

problem_questions = []

# 扫描所有题目
for q in questions:
    q_id = q.get('id')
    options = q.get('options', [])
    
    # 检查选项E（索引4）
    if len(options) > 4:
        opt_e = options[4]
        
        # 检查是否包含问题关键词
        for keyword in problem_keywords:
            if keyword in opt_e:
                problem_questions.append({
                    'id': q_id,
                    'option_e': opt_e,
                    'keyword': keyword
                })
                break

# 输出结果
print(f"发现 {len(problem_questions)} 道有问题的AP Micro题目：\n")
for pq in problem_questions:
    print(f"题目ID: {pq['id']}")
    print(f"选项E: {pq['option_e']}")
    print(f"问题关键词: {pq['keyword']}")
    print("-" * 80)

if len(problem_questions) == 0:
    print("太棒了！AP Micro没有发现类似问题！")
