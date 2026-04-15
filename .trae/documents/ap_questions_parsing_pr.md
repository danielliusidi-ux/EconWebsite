# AP经济学题库解析与数据处理需求文档

## 1. 项目概述

本项目需要解析AP Microeconomics和AP Macroeconomics两个文本文件，提取500道微观经济学题目和500道宏观经济学题目，生成结构化的Python数据，用于替换app.py中的QUESTION_BANK。

## 2. 数据源文件

### 2.1 AP Micro.txt
- **总题数**: 500道
- **章节结构**:
  - Diagnostic Quiz: Questions 1-20
  - Chapter 1 Basic Economic Concepts: Questions 21-84
  - Chapter 2 Supply and Demand: Questions 85-187
  - Chapter 3 Production, Cost, and the Perfect Competition Model: Questions 188-276
  - Chapter 4 Imperfect Competition: Questions 277-354
  - Chapter 5 Factor Markets: Questions 355-439
  - Chapter 6 Market Failure and the Role of Government: Questions 440-500

### 2.2 AP Macro.txt
- **总题数**: 500道
- **章节结构**:
  - Diagnostic Quiz: Questions 1-20
  - Chapter 1 Basic Economic Concepts: Questions 1-70
  - Chapter 2 Economic Indicators and the Business Cycle: Questions 71-170
  - Chapter 3 National Income and Price Determination: Questions 171-230
  - Chapter 4 The Financial Sector: Questions 231-315
  - Chapter 5 Long-Run Consequences of Stabilization Policies: Questions 316-440
  - Chapter 6 Open Economy—International Trade and Finance: Questions 441-500

## 3. 文件格式分析

### 3.1 题目部分格式
```
1. 题目内容...
(A) 选项A内容
(B) 选项B内容
(C) 选项C内容
(D) 选项D内容
(E) 选项E内容
2. 下一题...
```

### 3.2 答案部分格式
答案从"Answers"标题后开始，格式为：
```
1. (A) Choice (A) is correct. 解释内容...
2. (B) Choice (B) is correct. 解释内容...
```

或
```
168. (A) Choice (A) is correct. 解释内容...
```

答案行特点：
- 以题号开头，后跟括号和答案字母
- 包含"Choice (X) is correct"或"The correct choice is (X)"等标识
- 后面跟着详细解释

## 4. 目标数据结构

每道题需要包含以下字段：
```python
{
    'id': int,                    # 题目ID，从1开始连续编号
    'question': str,              # 题目内容
    'options': List[str],         # 选项列表，5个选项(A-E)
    'answer': str,                # 正确答案，如 'A', 'B', 'C', 'D', 'E'
    'explanation': str,           # 答案解释
    'topic': str,                 # 主题/章节名称
    'section': str,               # 章节名称
    'difficulty': str             # 难度，如 'Easy', 'Medium', 'Hard'
}
```

## 5. 解析策略

### 5.1 章节映射

#### AP Micro章节映射
```python
MICRO_SECTIONS = {
    (1, 20): "Diagnostic Quiz",
    (21, 84): "Chapter 1 Basic Economic Concepts",
    (85, 187): "Chapter 2 Supply and Demand",
    (188, 276): "Chapter 3 Production, Cost, and the Perfect Competition Model",
    (277, 354): "Chapter 4 Imperfect Competition",
    (355, 439): "Chapter 5 Factor Markets",
    (440, 500): "Chapter 6 Market Failure and the Role of Government"
}
```

#### AP Macro章节映射
```python
MACRO_SECTIONS = {
    (1, 20): "Diagnostic Quiz",
    (21, 70): "Chapter 1 Basic Economic Concepts",
    (71, 170): "Chapter 2 Economic Indicators and the Business Cycle",
    (171, 230): "Chapter 3 National Income and Price Determination",
    (231, 315): "Chapter 4 The Financial Sector",
    (316, 440): "Chapter 5 Long-Run Consequences of Stabilization Policies",
    (441, 500): "Chapter 6 Open Economy—International Trade and Finance"
}
```

### 5.2 解析步骤

1. **读取文件**: 读取整个文本文件内容
2. **分割题目和答案**: 找到"Answers"标记，分割题目部分和答案部分
3. **解析题目**:
   - 使用正则表达式匹配题号开头的段落
   - 提取题目内容和5个选项(A)-(E)
4. **解析答案**:
   - 匹配答案行格式 `数字. (字母)`
   - 提取答案字母和解释文本
5. **合并数据**: 将题目和答案按题号匹配
6. **添加章节信息**: 根据题号范围确定section和topic

## 6. 输出要求

生成两个Python列表：
- `ap_micro`: 包含500道微观经济学题目
- `ap_macro`: 包含500道宏观经济学题目

列表格式应可直接复制到app.py中替换QUESTION_BANK。

## 7. 注意事项

1. 题目ID从1开始连续编号
2. 选项格式统一为列表，包含5个字符串元素
3. 解释文本需要清理，去除多余的换行符
4. 难度可以统一设置为'Medium'或根据关键词判断
5. 确保题目顺序与原文档一致
