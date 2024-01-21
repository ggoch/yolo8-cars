import os
import os.path as osp
import glob
import sys
import shutil
import cv2

from enum import Enum


class imageType(Enum):
    JPG = 1
    PNG = 2


def read_image_dir(image_dir, image_type=imageType.JPG):
    image_files = None

    if image_type == imageType.JPG:
        image_files = glob.glob(osp.join(image_dir, "*.jpg"))
    elif image_type == imageType.PNG:
        image_files = glob.glob(osp.join(image_dir, "*.png"))

    return image_files


def check_output_dir_already_exists(output_dir, auto_remove=False):
    if osp.exists(output_dir):
        if auto_remove:
            shutil.rmtree(output_dir)
        else:
            print("Output directory already exists:", output_dir)
            sys.exit(1)

    os.makedirs(output_dir)


def merge_dir_data(first_folder, second_folder, output_combined_folder):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_combined_folder):
        os.makedirs(output_combined_folder)

    for filename in os.listdir(first_folder):
        source_path = os.path.join(first_folder, filename)
        destination_path = os.path.join(output_combined_folder, filename)
        shutil.copy(source_path, destination_path)

    for filename in os.listdir(second_folder):
        source_path = os.path.join(second_folder, filename)
        destination_path = os.path.join(output_combined_folder, filename)
        shutil.copy(source_path, destination_path)

    print("資料夾檔案合併完成：", output_combined_folder)


# def normalize_labels(labels, image_width, image_height):
#     normalized_labels = []

#     for label in labels:
#         x_min, y_min, x_max, y_max = map(float, label.split())

#         # 标准化坐标值
#         x_min /= image_width
#         x_max /= image_width
#         y_min /= image_height
#         y_max /= image_height

#         # 将标准化后的坐标转换为字符串并添加到列表中
#         normalized_label = f"{x_min} {y_min} {x_max} {y_max}"
#         normalized_labels.append(normalized_label)

#     return normalized_labels
    
def normalize_labels(labels, image_width, image_height):
    normalized_labels = []

    for label in labels:
        # 分割标签通常包含多个点，每个点的坐标由空格分隔
        points = label.split()
        normalized_points = []

        # 获取类别标记（第一个值）
        class_label = points[0]

        for i in range(1, len(points), 2):
            x = float(points[i])
            y = float(points[i + 1])

            # 标准化坐标值
            x /= image_width
            y /= image_height

            # 添加标准化后的点坐标到列表中
            normalized_points.extend([x, y])

        # 将标准化后的点坐标列表转换为字符串并添加到列表中
        normalized_label = f"{class_label} {' '.join(map(str, normalized_points))}"
        normalized_labels.append(normalized_label)

    return normalized_labels


def process_labels(image_dir, label_dir, output_dir, image_type=imageType.JPG):
    file_type = ".jpg" if image_type == imageType.JPG else ".png"
    # 获取图像文件列表
    image_files = [file for file in os.listdir(image_dir) if file.endswith(file_type)]

    for image_file in image_files:
        # 构建图像文件路径和标签文件路径
        image_path = os.path.join(image_dir, image_file)
        label_file = os.path.splitext(image_file)[0] + ".txt"
        label_path = os.path.join(label_dir, label_file)

        # 读取标签文件中的原始标签数据
        with open(label_path, "r") as file:
            labels = file.read().splitlines()

        # 获取图像的宽度和高度，这里假设所有图像尺寸相同
        image = cv2.imread(image_path)
        image_height, image_width = image.shape[:2]

        # 调用标签标准化函数
        normalized_labels = normalize_labels(labels, image_width, image_height)

        # 构建标准化后的标签文件路径
        output_label_path = os.path.join(output_dir, label_file)

        # 将标准化后的标签保存到文件中
        with open(output_label_path, "w") as file:
            file.write("\n".join(normalized_labels))
        
        print("標籤處理完成:", output_label_path)
