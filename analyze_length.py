#!/usr/bin/env python3
"""
分析AP Macro题目的字数分布，找出合适的阈值
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

# 计算所有题目的总字数
total_words_list = []
for q in questions:
    question_text = q.get('question', '')
    options = q.get('options', [])
    
    question_word_count = len(question_text.split())
    options_word_count = sum(len(opt.split()) for opt in options)
    total_word_count = question_word_count + options_word_count
    
    total_words_list.append(total_word_count)

# 排序
total_words_list.sort()
n = len(total_words_list)

print("字数统计:")
print(f"  最少字数: {total_words_list[0]}")
print(f"  最多字数: {total_words_list[-1]}")
print(f"  平均字数: {sum(total_words_list)/n:.1f}")
print(f"  中位数: {total_words_list[n//2]}")

# 计算25%和75%分位数（确保各占25%）
index_25 = int(n * 0.25)
index_50 = int(n * 0.50)
index_75 = int(n * 0.75)

print(f"\n分位数分析:")
print(f"  25%分位数 (第{index_25}题): {total_words_list[index_25]}字")
print(f"  50%分位数 (第{index_50}题): {total_words_list[index_50]}字")
print(f"  75%分位数 (第{index_75}题): {total_words_list[index_75]}字")

# 测试不同阈值
print(f"\n不同阈值下的分布:")
for threshold1 in [35, 40, 45, 50]:
    for threshold2 in [55, 60, 65, 70]:
        easy_count = sum(1 for w in total_words_list if w <= threshold1)
        medium_count = sum(1 for w in total_words_list if threshold1 < w <= threshold2)
        hard_count = sum(1 for w in total_words_list if w > threshold2)
        
        easy_pct = easy_count / n * 100
        medium_pct = medium_count / n * 100
        hard_pct = hard_count / n * 100
        
        if easy_pct >= 25 and medium_pct >= 25 and hard_pct >= 25:
            print(f"  阈值 {threshold1}/{threshold2}: Easy={easy_count}({easy_pct:.1f}%), Medium={medium_count}({medium_pct:.1f}%), Hard={hard_count}({hard_pct:.1f}%) ✓")
        else:
            print(f"  阈值 {threshold1}/{threshold2}: Easy={easy_count}({easy_pct:.1f}%), Medium={medium_count}({medium_pct:.1f}%), Hard={hard_count}({hard_pct:.1f}%)")
