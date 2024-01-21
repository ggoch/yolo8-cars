import os
import glob

def add_prefix_to_images(directory, prefix):
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在")
        return

    # 获取目录中所有的 .jpg 文件
    image_files = glob.glob(os.path.join(directory, "*.jpg"))

    # 遍历所有文件并重命名
    for file_path in image_files:
        # 分离目录和文件名
        dir_name, file_name = os.path.split(file_path)
        # 构建新的文件名
        new_file_name = prefix + file_name
        new_file_path = os.path.join(dir_name, new_file_name)

        # 重命名文件
        os.rename(file_path, new_file_path)
        print(f"文件 {file_name} 已重命名为 {new_file_name}")

def add_prefix_to_txts(directory, prefix):
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在")
        return

    # 获取目录中所有的 .jpg 文件
    image_files = glob.glob(os.path.join(directory, "*.txt"))

    # 遍历所有文件并重命名
    for file_path in image_files:
        # 分离目录和文件名
        dir_name, file_name = os.path.split(file_path)
        # 构建新的文件名
        new_file_name = prefix + file_name
        new_file_path = os.path.join(dir_name, new_file_name)

        # 重命名文件
        os.rename(file_path, new_file_path)
        print(f"文件 {file_name} 已重命名为 {new_file_name}")

# directory = 'wbdatas/wb_images'  # 替换为你的图片目录路径
directory = 'wbdatas/wb_videos/yellow/1'  # 替换为你的图片目录路径
prefix = 'wb_01yellow'  # 替换为你想要的前缀
# add_prefix_to_images(directory, prefix)