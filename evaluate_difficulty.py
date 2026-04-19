#!/usr/bin/env python3
"""
评估AP Macro题目的难度
基于以下标准：
- Easy: 基础概念题，直接定义或简单识别
- Medium: 需要理解和应用概念，简单计算
- Hard: 需要综合分析，多步骤计算，图表分析
"""

import ast
import re

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

def evaluate_difficulty(q):
    """评估题目难度"""
    question_text = q.get('question', '').lower()
    explanation = q.get('explanation', '').lower()
    section = q.get('section', '')
    
    # Hard难度的关键词和模式
    hard_patterns = [
        r'calculate|calculation|comput|determin.*value|find.*value',
        r'if.*increase.*decrease|if.*decreas.*increas',
        r'according to the.*diagram|according to the.*chart|according to the.*table',
        r'refer to.*diagram|refer to.*chart|refer to.*table',
        r'which of the following.*occur|which.*happen',
        r'combination|simultaneous|both.*and',
        r'long.*run.*short.*run|short.*run.*long.*run',
        r'multiplier|crowding out|phillips curve|aggregate demand.*aggregate supply',
        r'exchange rate|foreign exchange|balance of payment|trade deficit|trade surplus',
        r'fiscal policy.*monetary policy|monetary policy.*fiscal policy',
        r'opportunity cost.*comparative advantage|comparative advantage.*opportunity cost',
    ]
    
    # Easy难度的关键词和模式
    easy_patterns = [
        r'is defined as|refers to|means|is called',
        r'which of the following is|which is',
        r'example of|type of|kind of',
        r'basic economic concept|simple|direct',
    ]
    
    # 检查是否为Hard
    for pattern in hard_patterns:
        if re.search(pattern, question_text) or re.search(pattern, explanation):
            return 'Hard'
    
    # 检查题目长度和复杂度
    word_count = len(question_text.split())
    if word_count > 30:
        return 'Hard'
    
    # 检查是否为Easy
    for pattern in easy_patterns:
        if re.search(pattern, question_text):
            return 'Easy'
    
    # 根据章节和题号分配默认难度
    question_id = q.get('id', 0)
    
    # Chapter 1 (1-70): 基础概念，前30题Easy，后40题Medium/Hard
    if 1 <= question_id <= 30:
        return 'Easy'
    elif 31 <= question_id <= 50:
        return 'Medium'
    elif 51 <= question_id <= 70:
        return 'Hard'
    
    # Chapter 2 (71-170): 经济指标，较复杂
    elif 71 <= question_id <= 90:
        return 'Easy'
    elif 91 <= question_id <= 130:
        return 'Medium'
    elif 131 <= question_id <= 170:
        return 'Hard'
    
    # Chapter 3 (171-230): 国民收入和价格决定
    elif 171 <= question_id <= 190:
        return 'Easy'
    elif 191 <= question_id <= 210:
        return 'Medium'
    elif 211 <= question_id <= 230:
        return 'Hard'
    
    # Chapter 4 (231-315): 金融部门
    elif 231 <= question_id <= 250:
        return 'Easy'
    elif 251 <= question_id <= 280:
        return 'Medium'
    elif 281 <= question_id <= 315:
        return 'Hard'
    
    # Chapter 5 (316-440): 长期稳定政策后果，最难
    elif 316 <= question_id <= 340:
        return 'Easy'
    elif 341 <= question_id <= 390:
        return 'Medium'
    elif 391 <= question_id <= 440:
        return 'Hard'
    
    # Chapter 6 (441-500): 开放经济
    elif 441 <= question_id <= 460:
        return 'Easy'
    elif 461 <= question_id <= 480:
        return 'Medium'
    elif 481 <= question_id <= 500:
        return 'Hard'
    
    return 'Medium'

# 评估每道题的难度
difficulty_counts = {'Easy': 0, 'Medium': 0, 'Hard': 0}
for q in questions:
    difficulty = evaluate_difficulty(q)
    q['difficulty'] = difficulty
    difficulty_counts[difficulty] += 1

print("\n难度分布:")
for diff, count in difficulty_counts.items():
    print(f"  {diff}: {count}题")

# 按章节统计难度分布
sections = {}
for q in questions:
    section = q.get('section', 'Unknown')
    if section not in sections:
        sections[section] = {'Easy': 0, 'Medium': 0, 'Hard': 0}
    sections[section][q['difficulty']] += 1

print("\n各章节难度分布:")
for section, counts in sorted(sections.items()):
    print(f"  {section}:")
    for diff, count in counts.items():
        print(f"    {diff}: {count}题")

# 更新app.py
new_list_str = repr(questions)
new_content = content[:list_start] + new_list_str + content[list_end+1:]

with open('/Users/bytedance/Desktop/SideProject/EconWebsite/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n更新完成！题目难度已评估并更新。")
