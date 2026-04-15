#!/usr/bin/env python3
"""
仅基于字数评估来设置题目难度
"""

import re

# 读取parsed_questions.py
with open('parsed_questions.py', 'r', encoding='utf-8') as f:
    content = f.read()

def calculate_difficulty(question_data):
    """
    仅基于字数计算难度
    返回: 'Easy', 'Medium', 或 'Hard'
    """
    question = question_data.get('question', '')
    options = question_data.get('options', [])
    
    # 只考虑题目和选项（不包括解释）
    full_text = question + ' ' + ' '.join(options)
    
    # 计算字数（单词数）
    word_count = len(full_text.split())
    # 计算字符数
    char_count = len(full_text)
    
    # 仅基于字数评估难度
    # Hard: 字数 > 80词 或 字符数 > 400
    # Medium: 字数 > 50词 或 字符数 > 250
    # Easy: 其他
    
    if word_count > 80 or char_count > 400:
        return 'Hard'
    elif word_count > 50 or char_count > 250:
        return 'Medium'
    else:
        return 'Easy'

# 解析题目数据并更新难度
import ast

# 提取ap_micro数据
ap_micro_match = re.search(r'ap_micro = (\[.*?\])(?=\n\n|\Z)', content, re.DOTALL)
ap_macro_match = re.search(r'ap_macro = (\[.*?\])(?=\n\n|\Z)', content, re.DOTALL)

if ap_micro_match and ap_macro_match:
    ap_micro_list = ast.literal_eval(ap_micro_match.group(1))
    ap_macro_list = ast.literal_eval(ap_macro_match.group(1))
    
    # 更新难度
    for q in ap_micro_list:
        q['difficulty'] = calculate_difficulty(q)
    
    for q in ap_macro_list:
        q['difficulty'] = calculate_difficulty(q)
    
    # 统计难度分布
    micro_easy = sum(1 for q in ap_micro_list if q['difficulty'] == 'Easy')
    micro_medium = sum(1 for q in ap_micro_list if q['difficulty'] == 'Medium')
    micro_hard = sum(1 for q in ap_micro_list if q['difficulty'] == 'Hard')
    
    macro_easy = sum(1 for q in ap_macro_list if q['difficulty'] == 'Easy')
    macro_medium = sum(1 for q in ap_macro_list if q['difficulty'] == 'Medium')
    macro_hard = sum(1 for q in ap_macro_list if q['difficulty'] == 'Hard')
    
    print(f"AP Micro 难度分布:")
    print(f"  Easy: {micro_easy} ({micro_easy/len(ap_micro_list)*100:.1f}%)")
    print(f"  Medium: {micro_medium} ({micro_medium/len(ap_micro_list)*100:.1f}%)")
    print(f"  Hard: {micro_hard} ({micro_hard/len(ap_micro_list)*100:.1f}%)")
    
    print(f"\nAP Macro 难度分布:")
    print(f"  Easy: {macro_easy} ({macro_easy/len(ap_macro_list)*100:.1f}%)")
    print(f"  Medium: {macro_medium} ({macro_medium/len(ap_macro_list)*100:.1f}%)")
    print(f"  Hard: {macro_hard} ({macro_hard/len(ap_macro_list)*100:.1f}%)")
    
    # 生成新的Python代码
    def generate_code(questions, var_name):
        lines = [f"{var_name} = ["]
        for q in questions:
            lines.append("    {")
            for key, value in q.items():
                if isinstance(value, str):
                    lines.append(f"        '{key}': {repr(value)},")
                elif isinstance(value, list):
                    lines.append(f"        '{key}': {value},")
                else:
                    lines.append(f"        '{key}': {value},")
            lines.append("    },")
        lines.append("]")
        return '\n'.join(lines)
    
    new_content = f"# AP Microeconomics Questions ({len(ap_micro_list)})\n"
    new_content += generate_code(ap_micro_list, 'ap_micro')
    new_content += '\n\n'
    new_content += f"# AP Macroeconomics Questions ({len(ap_macro_list)})\n"
    new_content += generate_code(ap_macro_list, 'ap_macro')
    
    # 保存
    with open('parsed_questions_with_difficulty.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("\n已保存到 parsed_questions_with_difficulty.py")
    
    # 同时更新app.py
    # 构建新的QUESTION_BANK
    new_question_bank = f"""QUESTION_BANK = {{
    'ap_micro': {ap_micro_list},
    'ap_macro': {ap_macro_list}
}}"""
    
    # 读取app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # 找到QUESTION_BANK并替换
    start_marker = "QUESTION_BANK = {"
    start_idx = app_content.find(start_marker)
    if start_idx != -1:
        brace_count = 0
        end_idx = start_idx
        for i, char in enumerate(app_content[start_idx:]):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = start_idx + i + 1
                    break
        
        updated_content = app_content[:start_idx] + new_question_bank + app_content[end_idx:]
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("已更新 app.py 中的题目难度")
else:
    print("错误: 无法解析题目数据")
