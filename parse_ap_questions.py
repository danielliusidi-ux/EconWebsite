#!/usr/bin/env python3
"""
AP经济学题库解析脚本
解析AP Micro.txt和AP Macro.txt文件，生成结构化的题目数据
"""

import re
from typing import List, Dict, Tuple

# AP Micro章节映射
MICRO_SECTIONS = {
    (1, 20): "Diagnostic Quiz",
    (21, 84): "Chapter 1 Basic Economic Concepts",
    (85, 187): "Chapter 2 Supply and Demand",
    (188, 276): "Chapter 3 Production, Cost, and the Perfect Competition Model",
    (277, 354): "Chapter 4 Imperfect Competition",
    (355, 439): "Chapter 5 Factor Markets",
    (440, 500): "Chapter 6 Market Failure and the Role of Government"
}

# AP Macro章节映射
MACRO_SECTIONS = {
    (1, 20): "Diagnostic Quiz",
    (21, 70): "Chapter 1 Basic Economic Concepts",
    (71, 170): "Chapter 2 Economic Indicators and the Business Cycle",
    (171, 230): "Chapter 3 National Income and Price Determination",
    (231, 315): "Chapter 4 The Financial Sector",
    (316, 440): "Chapter 5 Long-Run Consequences of Stabilization Policies",
    (441, 500): "Chapter 6 Open Economy—International Trade and Finance"
}


def get_section(question_id: int, sections_map: dict) -> str:
    """根据题号获取章节名称"""
    for (start, end), section in sections_map.items():
        if start <= question_id <= end:
            return section
    return "Unknown"


def clean_text(text: str) -> str:
    """清理文本，去除多余空白和特殊字符"""
    text = ' '.join(text.split())
    text = text.replace('\f', '').replace('\x0c', '')
    return text.strip()


def parse_questions_from_text(text: str, start_id: int = 1, end_id: int = 500) -> Dict[int, Dict]:
    """
    从文本中解析题目
    只解析题目部分，不解析答案部分
    """
    questions = {}
    
    # 首先将分页符替换为换行符，避免跨页的题目被错误合并
    text = re.sub(r'[\f\x0c]+', '\n', text)
    
    # 题目格式: 数字. 题目内容（可能跨多行）(A) ... (B) ... (C) ... (D) ... (E) ...
    # 使用更精确的模式，确保匹配到完整的题目
    question_pattern = r'(?m)^(?P<num>\d+)\.\s+(?P<text>.+?)(?=\n\d+\.\s|\Z)'
    
    for match in re.finditer(question_pattern, text, re.DOTALL):
        num_str = match.group('num')
        q_text = match.group('text')
        q_num = int(num_str)
        
        # 只处理指定范围内的题目
        if q_num < start_id or q_num > end_id:
            continue
        
        # 清理文本，但保留换行符以便更好地识别结构
        q_text = ' '.join(q_text.split())
        
        # 跳过答案格式的内容（以(字母) Choice开头或包含"is correct"）
        if re.match(r'^\([A-E]\)\s*Choice', q_text) or \
           ('is correct' in q_text and 'Choice' in q_text[:50]):
            continue
        
        # 提取选项 - 使用更精确的模式
        options = []
        # 匹配 (A) ... (B) ... (C) ... (D) ... (E) ... 的模式
        option_pattern = r'\(([A-E])\)\s*([^()]+?)(?=\s*\([A-E]\)|\s*$)'
        option_matches = re.findall(option_pattern, q_text)
        
        if len(option_matches) >= 5:
            # 提取前5个选项
            for i, (letter, opt_text) in enumerate(option_matches[:5]):
                opt_text = clean_text(opt_text)
                # 检查选项文本是否包含下一个题号（如 "279."）
                next_q_match = re.search(r'\d+\.\s*\w', opt_text)
                if next_q_match and i == 4:  # 如果是第5个选项且包含题号
                    # 截断选项文本
                    opt_text = opt_text[:next_q_match.start()].strip()
                options.append(f"({letter}) {opt_text}")
            
            # 提取题目内容
            first_option_pos = q_text.find('(A)')
            if first_option_pos > 0:
                question_text = q_text[:first_option_pos].strip()
                question_text = clean_text(question_text)
                
                questions[q_num] = {
                    'question': question_text,
                    'options': options
                }
    
    return questions


def parse_answers_from_text(text: str, start_id: int = 1, end_id: int = 500) -> Dict[int, Dict]:
    """
    从文本中解析答案
    """
    answers = {}
    
    # 清理文本 - 将分页符替换为换行符
    clean_text_content = re.sub(r'[\f\x0c]+', '\n', text)
    
    # 答案格式1: 数字. (Unit: ...) ANSWER: (字母) 解释
    # 支持多行格式：数字. (Unit: ...)\nANSWER: (字母) 解释
    answer_pattern1 = r'(?m)^(?P<num>\d+)\.\s*\([^)]+\)(?:\s*See[^)]+\))?\s*\n?\s*(?:ANSWER:\s*)?\((?P<ans>[A-E])\)\s*(?P<exp>.+?)(?=\n\d+\.\s|\Z)'
    
    for match in re.finditer(answer_pattern1, clean_text_content, re.DOTALL):
        num_str = match.group('num')
        ans_letter = match.group('ans')
        explanation = match.group('exp')
        a_num = int(num_str)
        
        if a_num < start_id or a_num > end_id:
            continue
        
        explanation = clean_text(explanation)
        explanation = re.sub(r'^(?:Choice\s*\([A-E]\)\s*is\s*(?:the\s*)?(?:correct\s*)?(?:answer\s*)?\.?\s*)', '', explanation, flags=re.IGNORECASE)
        explanation = re.sub(r'^(?:The\s*correct\s*choice\s*is\s*\([A-E]\)\.?\s*)', '', explanation, flags=re.IGNORECASE)
        
        answers[a_num] = {
            'answer': ans_letter,
            'explanation': explanation
        }
    
    # 答案格式2: 数字. (Chapter X: ...) (字母) 解释
    answer_pattern2 = r'(?m)^(?P<num>\d+)\.\s*(?:\(Chapter\s*\d+:[^)]+\)\s*)?\((?P<ans>[A-E])\)\s*(?P<exp>.+?)(?=\n\d+\.\s|\Z)'
    
    for match in re.finditer(answer_pattern2, clean_text_content, re.DOTALL):
        num_str = match.group('num')
        ans_letter = match.group('ans')
        explanation = match.group('exp')
        a_num = int(num_str)
        
        if a_num < start_id or a_num > end_id:
            continue
        
        if a_num not in answers:
            explanation = clean_text(explanation)
            answers[a_num] = {
                'answer': ans_letter,
                'explanation': explanation
            }
    
    return answers


def parse_ap_file(file_path: str, sections_map: dict) -> List[Dict]:
    """
    解析AP题目文件
    文件结构：
    1. 前言和目录
    2. Diagnostic Quiz Questions (题号 1-20)
    3. Diagnostic Quiz Answers (题号 1-20)
    4. Chapter 1-6 Questions (题号 21-500)
    5. Chapter 1-6 Answers (题号 21-500)
    """
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"文件总长度: {len(content)} 字符")
    
    # 找到Diagnostic Quiz Questions开始位置
    quiz_questions_match = re.search(r'DIAGNOSTIC QUIZ\s+QUESTIONS', content, re.IGNORECASE)
    if not quiz_questions_match:
        raise ValueError(f"无法找到Diagnostic Quiz Questions: {file_path}")
    
    # 找到Diagnostic Quiz Answers开始位置
    quiz_answers_match = re.search(r'DIAGNOSTIC QUIZ\s+ANSWERS', content, re.IGNORECASE)
    if not quiz_answers_match:
        raise ValueError(f"无法找到Diagnostic Quiz Answers: {file_path}")
    
    # 找到Chapter Answers开始位置（单独的 "ANSWERS" 行，后面跟着 "Chapter X"）
    chapter_answers_match = re.search(r'\n\s*ANSWERS\s*\n\s*Chapter\s+\d+', content, re.IGNORECASE)
    
    # 提取Diagnostic Quiz题目（1-20题）
    diagnostic_questions_text = content[quiz_questions_match.end():quiz_answers_match.start()]
    
    # 提取Diagnostic Quiz答案（1-20题）
    if chapter_answers_match:
        diagnostic_answers_text = content[quiz_answers_match.end():chapter_answers_match.start()]
    else:
        diagnostic_answers_text = content[quiz_answers_match.end():]
    
    print(f"Diagnostic Quiz题目文本长度: {len(diagnostic_questions_text)} 字符")
    print(f"Diagnostic Quiz答案文本长度: {len(diagnostic_answers_text)} 字符")
    
    # 解析Diagnostic Quiz
    diagnostic_questions = parse_questions_from_text(diagnostic_questions_text, 1, 20)
    diagnostic_answers = parse_answers_from_text(diagnostic_answers_text, 1, 20)
    
    print(f"Diagnostic Quiz: 解析了 {len(diagnostic_questions)} 道题目, {len(diagnostic_answers)} 个答案")
    
    # 提取Chapter题目和答案（21-500题）
    all_questions = dict(diagnostic_questions)
    all_answers = dict(diagnostic_answers)
    
    if chapter_answers_match:
        # Chapter题目在Diagnostic Quiz Answers之后，Chapter Answers之前
        chapter_questions_start = quiz_answers_match.end()
        
        # 查找21题的位置来确认题目部分的开始
        q21_match = re.search(r'\n21\.\s', content[chapter_questions_start:chapter_answers_match.start()])
        if q21_match:
            chapter_questions_start = chapter_questions_start + q21_match.start()
        
        chapter_questions_text = content[chapter_questions_start:chapter_answers_match.start()]
        # Chapter答案在chapter_answers_match之后
        chapter_answers_text = content[chapter_answers_match.end():]
        
        print(f"Chapter题目文本长度: {len(chapter_questions_text)} 字符")
        print(f"Chapter答案文本长度: {len(chapter_answers_text)} 字符")
        
        # 解析Chapter题目（21-500题）
        chapter_questions = parse_questions_from_text(chapter_questions_text, 21, 500)
        # 解析Chapter答案（21-500题）
        chapter_answers = parse_answers_from_text(chapter_answers_text, 21, 500)
        
        all_questions.update(chapter_questions)
        all_answers.update(chapter_answers)
        
        print(f"Chapter Questions: 解析了 {len(chapter_questions)} 道题目")
        print(f"Chapter Answers: 解析了 {len(chapter_answers)} 个答案")
    
    print(f"总计: {len(all_questions)} 道题目, {len(all_answers)} 个答案")
    
    # 合并题目和答案
    result = []
    missing_answers = []
    
    for q_id in sorted(all_questions.keys()):
        if q_id in all_answers:
            q_data = all_questions[q_id]
            a_data = all_answers[q_id]
            section = get_section(q_id, sections_map)
            
            result.append({
                'id': q_id,
                'question': q_data['question'],
                'options': q_data['options'],
                'answer': a_data['answer'],
                'explanation': a_data['explanation'],
                'topic': section,
                'section': section,
                'difficulty': 'Medium'
            })
        else:
            missing_answers.append(q_id)
    
    if missing_answers:
        print(f"警告: {len(missing_answers)} 道题目缺少答案: {missing_answers[:20]}...")
    
    return result


def generate_python_code(questions: List[Dict], var_name: str) -> str:
    """生成Python代码字符串"""
    lines = [f"{var_name} = ["]
    
    for q in questions:
        lines.append("    {")
        lines.append(f"        'id': {q['id']},")
        lines.append(f"        'question': {repr(q['question'])},")
        lines.append(f"        'options': {repr(q['options'])},")
        lines.append(f"        'answer': {repr(q['answer'])},")
        lines.append(f"        'explanation': {repr(q['explanation'])},")
        lines.append(f"        'topic': {repr(q['topic'])},")
        lines.append(f"        'section': {repr(q['section'])},")
        lines.append(f"        'difficulty': {repr(q['difficulty'])}")
        lines.append("    },")
    
    lines.append("]")
    return '\n'.join(lines)


def validate_questions(questions: List[Dict], expected_count: int, name: str):
    """验证题目数据"""
    print(f"\n=== 验证 {name} ===")
    
    actual_count = len(questions)
    print(f"题目数量: {actual_count} / {expected_count}")
    if actual_count != expected_count:
        print(f"警告: 题目数量不匹配!")
    
    ids = [q['id'] for q in questions]
    expected_ids = list(range(1, expected_count + 1))
    missing_ids = set(expected_ids) - set(ids)
    if missing_ids:
        print(f"警告: 缺少题目ID: {sorted(missing_ids)[:20]}...")
    else:
        print("ID连续性: 通过")
    
    incomplete_options = [q['id'] for q in questions if len(q.get('options', [])) != 5]
    if incomplete_options:
        print(f"警告: 以下题目选项不完整: {incomplete_options[:10]}...")
    else:
        print("选项完整性: 通过 (每道题5个选项)")
    
    invalid_answers = [q['id'] for q in questions if q.get('answer') not in ['A', 'B', 'C', 'D', 'E']]
    if invalid_answers:
        print(f"警告: 以下题目答案无效: {invalid_answers[:10]}...")
    else:
        print("答案有效性: 通过")
    
    # 检查是否有题目内容看起来像答案解析
    suspicious_questions = []
    for q in questions:
        q_text = q.get('question', '')
        if re.match(r'^\([A-E]\)\s*Choice', q_text) or \
           ('is correct' in q_text and 'Choice' in q_text[:50]):
            suspicious_questions.append(q['id'])
    
    if suspicious_questions:
        print(f"警告: 以下题目内容可能是答案解析而非题目: {suspicious_questions[:10]}...")
    else:
        print("题目内容检查: 通过")
    
    sections = {}
    for q in questions:
        section = q.get('section', 'Unknown')
        sections[section] = sections.get(section, 0) + 1
    print("章节分布:")
    for section, count in sorted(sections.items()):
        print(f"  - {section}: {count} 题")


if __name__ == '__main__':
    print("=" * 60)
    print("AP经济学题库解析")
    print("=" * 60)
    
    print("\n>>> 解析 AP Micro.txt")
    try:
        ap_micro = parse_ap_file('AP Micro.txt', MICRO_SECTIONS)
        validate_questions(ap_micro, 500, "AP Micro")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        ap_micro = []
    
    print("\n>>> 解析 AP Macro.txt")
    try:
        ap_macro = parse_ap_file('AP Macro.txt', MACRO_SECTIONS)
        validate_questions(ap_macro, 500, "AP Macro")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        ap_macro = []
    
    print("\n>>> 生成Python代码")
    micro_code = generate_python_code(ap_micro, 'ap_micro')
    macro_code = generate_python_code(ap_macro, 'ap_macro')
    
    output_file = 'parsed_questions.py'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# AP Microeconomics Questions (500)\n")
        f.write(micro_code)
        f.write('\n\n')
        f.write("# AP Macroeconomics Questions (500)\n")
        f.write(macro_code)
    
    print(f"\n已保存到: {output_file}")
    print(f"AP Micro: {len(ap_micro)} 道题目")
    print(f"AP Macro: {len(ap_macro)} 道题目")
