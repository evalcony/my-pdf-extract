# my-pdf-extract
pdf的内容提取，提取其中的图片+文字


### 介绍

本项目是对图片进行识别。所以，需要将pdf先转为分页+图片。这是另一个前置项目的工作。

整个项目的思路是基于`OCR`的。因为实验了很多对pdf直接解析的库，会由于当前页面中文字部分过少而无法准确识别，将图文混合在一起，以至于不可用。

### 使用方法

```
python3 ocr.py -i input_file -o output_file
```

### 文件

`resources` 目录下放置测试内容资源文件。
`output` 目录下放置输出结果。


### 算法

由于需求涉及到的 pdf 内容的独特性（1图+若干文字），故采取了「最大圈地面积」算法。

这个算法的基本思路是：

1. 将图像转为灰度图，做二值化处理。由于背景不一定是纯白，所以在做二值化处理时要有一定的误差容忍性。

2. 遍历图片像素，找到最大的「连通块」，这个就视为图片。注意，要将白色背景所在的「连通块」排除。

3. 最后，将图片所在的矩形块，保存下来即可。

至于文字的提取则很容易，是用`pytesseract`这个库做的。
