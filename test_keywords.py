#!/usr/bin/env python3
"""
测试改进后的关键词搜索
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

# 同义词词典（跟app.py一致）
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
    
    expanded_keywords = []
    for kw in keywords:
        expanded_keywords.append(kw)
        if kw in SYNONYMS:
            expanded_keywords.extend(SYNONYMS[kw])
    
    expanded_keywords = list(set(expanded_keywords))
    
    filtered = []
    for q in questions:
        text = ' '.join([
            q.get('question', ''),
            ' '.join(q.get('options', [])),
            q.get('explanation', '')
        ]).lower()
        if any(kw in text for kw in expanded_keywords):
            filtered.append(q)
    return filtered

print(f"总共有 {len(questions)} 道AP Macro题目\n")

# 测试搜索"CPI"
cpi_result = filter_by_keywords(questions, "CPI")
print(f"搜索 'CPI' 找到 {len(cpi_result)} 道题目:")
for q in cpi_result:
    print(f"  ID: {q['id']} - {q['question'][:60]}...")

print("\n" + "="*80 + "\n")

# 测试搜索"GDP"
gdp_result = filter_by_keywords(questions, "GDP")
print(f"搜索 'GDP' 找到 {len(gdp_result)} 道题目")

print("\n" + "="*80 + "\n")

# 测试搜索"inflation"
inflation_result = filter_by_keywords(questions, "inflation")
print(f"搜索 'inflation' 找到 {len(inflation_result)} 道题目")
