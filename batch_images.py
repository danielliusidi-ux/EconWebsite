#!/usr/bin/env python3
"""
批量处理题目图片的工具脚本
使用方法：
1. 将所有从PDF提取的图片放在一个文件夹中
2. 按照题目ID重命名图片：question_1.png, question_2.png, ...
3. 运行此脚本自动整理图片到正确的文件夹
"""

import os
import shutil
import re

def batch_organize_images(source_folder, exam_type='ap_micro'):
    """
    批量整理图片到正确的文件夹
    
    Args:
        source_folder: 包含原始图片的文件夹路径
        exam_type: 'ap_micro' 或 'ap_macro'
    """
    # 创建目标文件夹
    target_folder = f'static/images/{exam_type}'
    os.makedirs(target_folder, exist_ok=True)
    
    # 支持的图片格式
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    
    # 获取源文件夹中的所有图片
    images = [f for f in os.listdir(source_folder) 
              if f.lower().endswith(image_extensions)]
    
    if not images:
        print(f"❌ 在 {source_folder} 中没有找到图片文件")
        return
    
    print(f"✅ 找到 {len(images)} 张图片")
    
    # 处理每张图片
    moved_count = 0
    for filename in images:
        # 尝试从文件名中提取题目ID
        # 支持格式：question_1.png, q1.png, 1.png, question1.png 等
        match = re.search(r'(\d+)', filename)
        
        if match:
            question_id = match.group(1)
            ext = os.path.splitext(filename)[1]
            
            # 目标文件名
            target_filename = f'question_{question_id}{ext.lower()}'
            target_path = os.path.join(target_folder, target_filename)
            source_path = os.path.join(source_folder, filename)
            
            # 复制文件
            shutil.copy2(source_path, target_path)
            print(f"✅ 已复制: {filename} -> {target_filename}")
            moved_count += 1
        else:
            print(f"⚠️  无法从 {filename} 中提取题目ID，跳过")
    
    print(f"\n🎉 完成！共处理 {moved_count} 张图片")
    print(f"📁 图片已保存到: {target_folder}")

def generate_image_mapping(exam_type='ap_micro'):
    """
    生成题目ID到图片路径的映射
    用于快速更新 app.py 中的题目数据
    """
    image_folder = f'static/images/{exam_type}'
    
    if not os.path.exists(image_folder):
        print(f"❌ 文件夹不存在: {image_folder}")
        return {}
    
    image_mapping = {}
    
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            match = re.search(r'question_(\d+)', filename)
            if match:
                question_id = int(match.group(1))
                image_mapping[question_id] = f'images/{exam_type}/{filename}'
    
    print(f"✅ 生成了 {len(image_mapping)} 个题目的图片映射")
    
    # 打印可以直接复制到 app.py 的代码
    print("\n📝 可以复制以下代码到 app.py:")
    print("-" * 60)
    for qid, img_path in sorted(image_mapping.items()):
        print(f"        'id': {qid},")
        print(f"        'image': '{img_path}',")
        print("-" * 40)
    
    return image_mapping

if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("📚 题目图片批量处理工具")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n使用方法:")
        print("  1. 整理图片: python batch_images.py organize <源文件夹> [ap_micro|ap_macro]")
        print("  2. 生成映射: python batch_images.py mapping [ap_micro|ap_macro]")
        print("\n示例:")
        print("  python batch_images.py organize ~/Downloads/pdf_images ap_micro")
        print("  python batch_images.py mapping ap_micro")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'organize':
        if len(sys.argv) < 3:
            print("❌ 请指定源文件夹路径")
            sys.exit(1)
        
        source_folder = sys.argv[2]
        exam_type = sys.argv[3] if len(sys.argv) > 3 else 'ap_micro'
        
        if not os.path.exists(source_folder):
            print(f"❌ 源文件夹不存在: {source_folder}")
            sys.exit(1)
        
        batch_organize_images(source_folder, exam_type)
    
    elif command == 'mapping':
        exam_type = sys.argv[2] if len(sys.argv) > 2 else 'ap_micro'
        generate_image_mapping(exam_type)
    
    else:
        print(f"❌ 未知命令: {command}")
