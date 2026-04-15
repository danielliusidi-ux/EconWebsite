# 题目图表添加说明

## 步骤 1：保存图片

1. 将你提供的 production possibilities curve 图片保存到：
   - `static/images/ap_micro/` 文件夹
2. 重命名文件为：`question_4.png`

## 步骤 2：更新题目数据

在 `app.py` 中，找到第 4 题，添加 `image` 字段：

```python
{
    'id': 4,
    'question': 'The concave shape of the production possibilities curve implies the notion of',
    'options': ['A) increasing opportunity costs', 'B) comparative advantage', 'C) marginal analysis', 'D) allocation of limited resources with unlimited material wants', 'E) MB = MC'],
    'answer': 'A',
    'explanation': 'Choice (A) is correct because the production possibilities curve represents the maximum output between two goods using scarce resources. As such, it represents the increasing opportunity costs incurred when the production shifts to more of one product than the other. The more a producer chooses to make of a product, the more the opportunity cost increases for the product not being produced. This represents the law of increasing costs.',
    'topic': 'Basic Economic Concepts',
    'section': 'Basic Economic Concepts',
    'difficulty': 'Easy',
    'image': 'images/ap_micro/question_4.png'  # 添加这一行
}
```

## 步骤 3：访问题目

刷新页面，访问第 4 题，你将看到图片显示在题目下方！

---

## 通用添加图片的方法

对于其他题目：

1. 从 PDF 中截图或导出图表
2. 保存到对应的文件夹：
   - AP Micro: `static/images/ap_micro/`
   - AP Macro: `static/images/ap_macro/`
3. 文件名格式：`question_{题目ID}.png` （例如：question_57.png）
4. 在 `app.py` 中给题目添加 `image` 字段
