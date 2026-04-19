#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, save_shared_quiz, get_shared_quiz
import uuid
import json

test_data = {
    'exam_type': 'ap_micro',
    'question_ids': [231, 232],
    'quiz_answers': {'231': 'C', '232': 'A'},
    'quiz_start_time': 123456789,
    'section': 'Chapter 1',
    'is_result': True
}

result_id = str(uuid.uuid4())
print(f"测试保存 result_id: {result_id}")
print(f"测试数据: {json.dumps(test_data, indent=2)}")

save_result = save_shared_quiz(result_id, test_data)
print(f"save_shared_quiz 返回: {save_result}")

print(f"\n尝试读取 result_id: {result_id}")
loaded_data = get_shared_quiz(result_id)
print(f"get_shared_quiz 返回: {loaded_data}")
if loaded_data:
    print(f"数据是否有 is_result: {loaded_data.get('is_result')}")

print(f"\n检查 SHARED_QUIZZES 字典 (内存存储):")
from app import SHARED_QUIZZES
print(f"内存中的键: {list(SHARED_QUIZZES.keys())}")
