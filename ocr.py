import os

import numpy as np
import pytesseract
import argparse
from skimage import measure
from PIL import Image

def save_pure_text(text, output_path):
	file = open(output_path, 'w')
	file.writelines(text)
	print(text)

def save_pure_img(input_path, output_path):
	largest_contour = find_largest_contour(input_path)
	save_cropped_image(largest_contour, output_path)

def find_largest_contour(image_path, tolerance=10):
    original_image = Image.open(image_path).convert("RGB")

    # 转换为灰度图像
    grayscale_image = original_image.convert("L")

    # 转换为NumPy数组
    image_array = np.array(grayscale_image)

    # 计算颜色的容差范围
    lower_bound = 255 - tolerance
    upper_bound = 255

    # 将背景颜色设置为0，其他颜色设置为1
    binary_image = ~(lower_bound <= image_array)

    # 标记连通区域
    labeled_image = measure.label(binary_image)

    # 找到面积最大的非背景区域
    regions = measure.regionprops(labeled_image)
    non_background_regions = [region for region in regions if region.area > 0]
    largest_region = max(non_background_regions, key=lambda prop: prop.area)

    # 获取最大区域的坐标
    minr, minc, maxr, maxc = largest_region.bbox

    # 提取最大区域的部分
    largest_contour = original_image.crop((minc, minr, maxc, maxr))

    return largest_contour

def save_cropped_image(cropped_image, output_path):
    # 创建一个相同大小的白底图片
    result_image = Image.new("RGB", cropped_image.size, (255, 255, 255))

    # 将裁剪的图形粘贴到白底图片上
    result_image.paste(cropped_image, (0, 0))

    # 保存结果图片
    result_image.save(output_path)


def main(args):
	input_path = args.i
	output_path = args.o

	output_text_format = "{output_path}/text/{file_name}.txt"
	output_img_format = "{output_path}/img/{file_name}.png"

	# img转txt
	files = os.listdir(input_path)
	for file in files:
		print(file)
		name = file.split('.')[0]
		image = Image.open(input_path+'/'+file)
		text = pytesseract.image_to_string(image)

		txt_output_path = output_text_format.replace('{output_path}', output_path).replace('{file_name}', name)
		img_output_path = output_img_format.replace('{output_path}', output_path).replace('{file_name}', name)

		save_pure_text(text, txt_output_path)
		save_pure_img(input_path+'/'+file, img_output_path)

		print('-' * 20)

if __name__ == '__main__':
	# 读取参数
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', type=str, default='', help='追加参数')
	parser.add_argument('-o', type=str, default='', help='追加参数')
	# parser.add_argument('-f', action='store_true', help='无追加参数')
	args = parser.parse_args()

	main(args)

