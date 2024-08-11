import os

def scan_and_rename_images(folder_path, keyword):
    # 获取文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 仅处理图片文件（假设图片文件以 .jpg 或 .png 结尾）
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # 检查文件名中是否包含关键字
            if keyword not in filename:
                # 构建新的文件名
                new_filename = f"{os.path.splitext(filename)[0]}_{keyword}{os.path.splitext(filename)[1]}"
                # 获取完整路径
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)
                # 重命名文件
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")
            else:
                print(f"Skipped: {filename}")

scan_and_rename_images("datasets/custom/train/rubbish_truck", "rubbish_truck")