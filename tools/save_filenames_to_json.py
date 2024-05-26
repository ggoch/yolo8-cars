import os
import json

def save_filenames_to_json(folder_path, output_json_path):
    # 获取指定文件夹下的所有文件名
    filenames = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filenames.append(file)

    # 将文件名数组保存为JSON文件
    with open(output_json_path, 'w') as json_file:
        json.dump(filenames, json_file, indent=4)
        print(f"已将文件名保存到JSON文件: {output_json_path}")

# 使用示例
folder_path = './datas/labelme_thing'  # 替换为您的文件夹路径
output_json_path = 'labelme_thing_record.json'  # 输出的JSON文件路径

save_filenames_to_json(folder_path, output_json_path)