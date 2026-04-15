# 📸 题目图片批量处理指南

## 方法一：使用 PDF 提取工具（推荐）

### 步骤 1：从 PDF 中批量提取图片

#### 选项 A：使用在线工具
1. 访问 https://www.ilovepdf.com/extract-images
2. 上传你的 AP Micro/Macro PDF 文件
3. 选择 "Extract images"
4. 下载提取的所有图片（通常是一个 ZIP 文件）

#### 选项 B：使用 Adobe Acrobat
1. 用 Adobe Acrobat 打开 PDF
2. 工具 → 导出 PDF → 图像 → JPEG 或 PNG
3. 选择导出位置

#### 选项 C：使用 Python（如果你熟悉）
```python
# 需要安装: pip install PyMuPDF
import fitz  # PyMuPDF

pdf_path = "your_file.pdf"
doc = fitz.open(pdf_path)

for page_num in range(len(doc)):
    page = doc[page_num]
    image_list = page.get_images()
    
    for img_idx, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        with open(f"page_{page_num+1}_img_{img_idx+1}.{image_ext}", "wb") as f:
            f.write(image_bytes)
```

---

## 方法二：使用我的批量处理脚本

### 步骤 1：准备图片文件夹
将从 PDF 提取的所有图片放到一个文件夹中，例如：
```
~/Downloads/pdf_images/
├── image1.png
├── image2.png
├── image3.png
└── ...
```

### 步骤 2：按照题目ID重命名图片

#### 快速重命名技巧（Mac）：
1. 选中所有图片
2. 右键 → 重命名
3. 选择 "格式" → "名称和索引"
4. 名称格式：`question_`
5. 起始编号：`1`
6. 点击重命名

结果应该是：
```
question_1.png
question_2.png
question_3.png
...
```

### 步骤 3：运行批量整理脚本

在终端中运行：

```bash
cd /Users/bytedance/Desktop/SideProject/EconWebsite

# 整理 AP Micro 的图片
python3 batch_images.py organize ~/Downloads/pdf_images ap_micro

# 或者整理 AP Macro 的图片
python3 batch_images.py organize ~/Downloads/pdf_images ap_macro
```

### 步骤 4：生成图片映射（可选，帮助你更新 app.py）

```bash
# 生成 AP Micro 的图片映射
python3 batch_images.py mapping ap_micro

# 生成 AP Macro 的图片映射
python3 batch_images.py mapping ap_macro
```

这会输出可以直接复制到 app.py 的代码格式！

---

## 方法三：手动但更精确的方法

如果你知道哪些题目对应哪些图片：

### 创建一个图片映射文件

创建 `image_mapping.json`：

```json
{
  "ap_micro": {
    "4": "images/ap_micro/question_4.png",
    "57": "images/ap_micro/question_57.png",
    "58": "images/ap_micro/question_58.png"
  },
  "ap_macro": {
    "10": "images/ap_macro/question_10.png"
  }
}
```

然后我可以帮你写一个脚本自动更新 app.py！

---

## 💡 小贴士

### 1. 快速找到带图表的题目
- 在 PDF 中浏览，记下带图表的题目编号
- 只提取这些页的图片

### 2. 使用截图工具（如果提取困难）
- Mac: `Cmd + Shift + 4` 然后拖动选择区域
- Windows: `Win + Shift + S`
- 截图后直接按照 question_X.png 命名

### 3. 验证图片
运行脚本后，访问对应的题目验证图片是否正确显示：
```
http://127.0.0.1:5001/practice/ap_micro?question_id=4
```

---

## 需要帮助？

如果你：
- 不知道如何从 PDF 提取图片
- 图片已经提取但不知道如何对应题目
- 想要更自动化的解决方案

告诉我，我可以帮你进一步优化流程！
