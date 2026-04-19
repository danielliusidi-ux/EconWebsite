#!/usr/bin/env python3
"""
完整测试generate_quiz流程
"""

import ast
import random
import json

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
questions_all = ast.literal_eval(list_str)

# 同义词词典
SYNONYMS = {
    'cpi': ['cpi', 'consumer price index'],
    'consumer': ['cpi', 'consumer price index'],
    'price': ['cpi', 'consumer price index'],
    'index': ['cpi', 'consumer price index'],
    'gdp': ['gdp', 'gross domestic product'],
    'gross': ['gdp', 'gross domestic product'],
    'domestic': ['gdp', 'gross domestic product'],
    'product': ['gdp', 'gross domestic product'],
    'unemployment': ['unemployment', 'unemployed'],
    'unemployed': ['unemployment', 'unemployed'],
    'inflation': ['inflation', 'inflated', 'price increase'],
    'interest': ['interest', 'interest rate'],
    'rate': ['interest', 'interest rate', 'exchange rate'],
    'exchange': ['exchange rate'],
    'fiscal': ['fiscal', 'fiscal policy'],
    'monetary': ['monetary', 'monetary policy'],
    'policy': ['fiscal policy', 'monetary policy'],
}

def filter_by_keywords(questions, keywords_str):
    if not keywords_str:
        return questions
    keywords = [kw.strip().lower() for kw in keywords_str.split() if kw.strip()]
    if not keywords:
        return questions
    
    filtered = []
    for q in questions:
        text = ' '.join([
            q.get('question', ''),
            ' '.join(q.get('options', [])),
            q.get('explanation', '')
        ]).lower()
        
        # 所有关键词都要匹配
        all_match = True
        for kw in keywords:
            # 检查该关键词及其同义词是否都匹配
            has_match = False
            
            # 检查原关键词
            if kw in text:
                has_match = True
            # 检查同义词
            elif kw in SYNONYMS:
                for syn in SYNONYMS[kw]:
                    if syn in text:
                        has_match = True
                        break
            
            if not has_match:
                all_match = False
                break
        
        if all_match:
            filtered.append(q)
    
    return filtered

print("=== 完整测试generate_quiz流程 ===\n")

# 模拟用户选择所有章节
selected_sections = list(set(q.get('section', '') for q in questions_all))
selected_sections.sort()
print(f"用户选择的章节: {len(selected_sections)} 个")

keywords_param = "loanable funds"
count = 10

print(f"\n搜索关键词: '{keywords_param}'")
print(f"题目数量: {count}\n")

# 按章节分组并应用关键词过滤
section_questions = {}
for s in selected_sections:
    section_qs = [q for q in questions_all if q.get('section') == s]
    filtered_qs = filter_by_keywords(section_qs, keywords_param)
    section_questions[s] = filtered_qs
    if filtered_qs:
        print(f"章节 '{s}': 找到 {len(filtered_qs)} 道题")
        for q in filtered_qs:
            print(f"  - ID: {q['id']}")

# 计算每个章节应该选多少题
num_sections = len(selected_sections)
questions_per_section = count // num_sections
remaining_questions = count % num_sections

print(f"\n每个章节分配: {questions_per_section} 道题")
print(f"剩余题目: {remaining_questions} 道")

# 从每个章节均匀随机挑选题目
selected_questions = []
for i, s in enumerate(selected_sections):
    q_list = section_questions[s]
    num_to_take = questions_per_section + (1 if i < remaining_questions else 0)
    num_to_take = min(num_to_take, len(q_list))
    random.shuffle(q_list)
    selected_questions.extend(q_list[:num_to_take])
    print(f"\n从章节 '{s}' 选择 {num_to_take} 道题:")
    for q in q_list[:num_to_take]:
        print(f"  - ID: {q['id']}")

print(f"\n最终选中的题目 ({len(selected_questions)} 道):")
for q in selected_questions:
    print(f"  - ID: {q['id']} - {q['question'][:60]}...")
