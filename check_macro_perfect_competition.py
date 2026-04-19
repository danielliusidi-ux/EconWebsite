#!/usr/bin/env python3
"""
检查AP Macro中有没有'perfect competition'
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

print(f"AP Macro总共有 {len(questions)} 道题目\n")

# 测试搜索 'perfect competition'
result = filter_by_keywords(questions, "perfect competition")
print(f"搜索 'perfect competition' 找到 {len(result)} 道题目\n")

# 也检查一下只搜索 'competition'
result_competition = filter_by_keywords(questions, "competition")
print(f"搜索 'competition' 找到 {len(result_competition)} 道题目\n")

# 显示包含'competition'的题目
if result_competition:
    print("包含'competition'的题目:")
    for q in result_competition[:10]:  # 只显示前10道
        print(f"  ID: {q['id']} - {q['question'][:60]}...")
