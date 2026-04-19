#!/usr/bin/env python3
"""
用正则表达式修复AP Micro题目选项E中的问题
"""

import re

# 读取app.py
with open('/Users/bytedance/Desktop/SideProject/EconWebsite/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义需要修复的题目和它们的正确选项E
fix_map = {
    42: "(E) barter economy",
    54: "(E) The curve would shift to the right and become concave.",
    56: "(E) 300 cookies",
    84: "(E) company D because it has the largest marginal revenue",
    95: "(E) at the price where either the demand or supply curve becomes horizontal",
    125: "(E) luxury goods",
    129: "(E) have no effect on the price of the good or quantity demanded",
    155: "(E) the area to the right of the supply curve and to the left of the demand curve",
    174: "(E) marginal benefits",
    187: "(E) only market E is perfectly competitive",
    276: "(E) $200, as this is how much the company can earn from an additional unit of vaccine.",
    316: "(E) sensitivity to the determinants of supply and demand and price level",
    337: "(E) leave the oil price and quantity supplied unchanged",
    354: "(E) There are numerous options for price differentiation.",
    366: "(E) negative externality",
    439: "(E) frosting quantity will decrease"
}

new_content = content
fixed_count = 0

for q_id, correct_opt_e in fix_map.items():
    # 先找到这道题的id
    pattern = r"'id':\s*" + str(q_id) + r",.*?'options':\s*\[.*?\]"
    
    # 找到这道题的完整内容
    match = re.search(pattern, new_content, re.DOTALL)
    if match:
        q_text = match.group(0)
        # 找到选项E
        opt_e_match = re.search(r"'[()]E\)[^']*?(?:'|,|\])", q_text)
        if opt_e_match:
            old_opt_e = opt_e_match.group(0)
            if old_opt_e != "'" + correct_opt_e + "'":
                # 替换
                new_opt_e = "'" + correct_opt_e + "'"
                new_q_text = q_text.replace(old_opt_e, new_opt_e)
                new_content = new_content.replace(q_text, new_q_text)
                print(f"修复题目 {q_id}")
                print(f"  原选项: {old_opt_e}")
                print(f"  新选项: {new_opt_e}")
                print()
                fixed_count += 1

# 写入文件
with open('/Users/bytedance/Desktop/SideProject/EconWebsite/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n更新完成！共修复了 {fixed_count} 道AP Micro题目。")
