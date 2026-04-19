#!/usr/bin/env python3
"""
按照题目字数+选项总字数评估AP Macro题目的难度
字数越长题目越难
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

def evaluate_difficulty_by_length(q):
    """按照题目字数+选项总字数评估难度"""
    question_text = q.get('question', '')
    options = q.get('options', [])
    
    # 计算题目字数
    question_word_count = len(question_text.split())
    
    # 计算所有选项的总字数
    options_word_count = 0
    for option in options:
        options_word_count += len(option.split())
    
    # 总字数 = 题目字数 + 选项总字数
    total_word_count = question_word_count + options_word_count
    
    # 根据总字数分配难度
    # Easy: 总字数较少，题目和选项都简单
    # Medium: 总字数中等，可能题目短但选项长，或题目长但选项短
    # Hard: 总字数多，题目复杂或选项需要仔细分析
    # 阈值设定确保各难度占比都≥25%: Easy≤40, Medium 41-55, Hard>55
    
    if total_word_count <= 40:
        return 'Easy'
    elif total_word_count <= 55:
        return 'Medium'
    else:
        return 'Hard'

# 评估每道题的难度
difficulty_counts = {'Easy': 0, 'Medium': 0, 'Hard': 0}
length_stats = []

for q in questions:
    difficulty = evaluate_difficulty_by_length(q)
    q['difficulty'] = difficulty
    difficulty_counts[difficulty] += 1
    
    question_text = q.get('question', '')
    options = q.get('options', [])
    
    question_word_count = len(question_text.split())
    options_word_count = sum(len(opt.split()) for opt in options)
    total_word_count = question_word_count + options_word_count
    
    length_stats.append({
        'id': q.get('id'),
        'question_words': question_word_count,
        'options_words': options_word_count,
        'total_words': total_word_count,
        'difficulty': difficulty
    })

print("\n难度分布:")
for diff, count in difficulty_counts.items():
    print(f"  {diff}: {count}题")

# 按章节统计难度分布
sections = {}
for q in questions:
    section = q.get('section', 'Unknown')
    if section not in sections:
        sections[section] = {'Easy': 0, 'Medium': 0, 'Hard': 0, 'total_words': 0, 'count': 0}
    sections[section][q['difficulty']] += 1
    
    question_text = q.get('question', '')
    options = q.get('options', [])
    total_words = len(question_text.split()) + sum(len(opt.split()) for opt in options)
    sections[section]['total_words'] += total_words
    sections[section]['count'] += 1

print("\n各章节难度分布:")
for section, data in sorted(sections.items()):
    avg_words = data['total_words'] / data['count'] if data['count'] > 0 else 0
    print(f"  {section}:")
    for diff in ['Easy', 'Medium', 'Hard']:
        print(f"    {diff}: {data[diff]}题")
    print(f"    平均总字数: {avg_words:.1f}")

# 显示总字数范围统计
print("\n总字数范围统计（题目+选项）:")
word_ranges = [
    (0, 40, '0-40字'),
    (41, 60, '41-60字'),
    (61, 80, '61-80字'),
    (81, 100, '81-100字'),
    (101, 120, '101-120字'),
    (121, 150, '121-150字'),
    (151, 200, '151-200字'),
    (201, 999, '200字以上')
]

for min_w, max_w, label in word_ranges:
    count = sum(1 for s in length_stats if min_w <= s['total_words'] <= max_w)
    print(f"  {label}: {count}题")

# 显示一些Hard题目的例子
print("\nHard难度题目示例:")
hard_examples = [s for s in length_stats if s['difficulty'] == 'Hard'][:5]
for ex in hard_examples:
    print(f"  ID {ex['id']}: 题目{ex['question_words']}字 + 选项{ex['options_words']}字 = 共{ex['total_words']}字")

# 更新app.py
new_list_str = repr(questions)
new_content = content[:list_start] + new_list_str + content[list_end+1:]

with open('/Users/bytedance/Desktop/SideProject/EconWebsite/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n更新完成！题目难度已按照题目+选项总字数评估并更新。")
