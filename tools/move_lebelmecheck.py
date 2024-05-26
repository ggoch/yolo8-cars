import os
import json
import shutil

def move_labelmecheck(source_folder, destination_folder,processed_files_path,clean_processed_files=True,move_file=True,delete_img=True):
    # 確認目標資料夾存在，若不存在則創建
    os.makedirs(destination_folder, exist_ok=True)

    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as f:
            processed_files = json.load(f)
    else:
        processed_files = []

    check_file_name_set = set(processed_files)

    # 清空已處理文件列表
    if clean_processed_files:
        for filename in os.listdir(source_folder):
            if filename in check_file_name_set:
                check_file_name_set.remove(filename)

                json_path = os.path.join(source_folder, filename)
                image_path = os.path.join(source_folder, filename.replace('.json', '.jpg'))  # 假設圖片為jpg格式，根據實際情況修改

                # 刪除JSON和圖片文件
                os.remove(json_path)
                if os.path.exists(image_path):
                    os.remove(image_path)
                print(f"已刪除已處理文件: {filename}")

    # 遍歷資料夾中的所有文件
    if move_file:
        for filename in os.listdir(source_folder):
            if filename.endswith('.json'):
                json_path = os.path.join(source_folder, filename)
                image_path = os.path.join(source_folder, filename.replace('.json', '.jpg'))  # 假設圖片為jpg格式，根據實際情況修改

                with open(json_path, 'r') as f:
                    data = json.load(f)

                # 檢查是否存在need標籤
                need_exists = any(shape.get('label') == 'need' for shape in data.get('shapes', []))

                # 檢查是否存在need標籤
                if need_exists:
                    # 刪除need標籤
                    data['shapes'] = [shape for shape in data['shapes'] if shape.get('label') != 'need']

                    # 搬移JSON和圖片文件到目標資料夾
                    shutil.move(json_path, os.path.join(destination_folder, filename))
                    if os.path.exists(image_path):
                        shutil.move(image_path, os.path.join(destination_folder, filename.replace('.json', '.jpg')))

                    # 寫回更新後的JSON文件
                    with open(os.path.join(destination_folder, filename), 'w') as f:
                        json.dump(data, f, indent=4)

                    # 添加文件到已處理文件列表
                    processed_files.append(filename)
                    print(f"已處理文件: {filename}")

                else:
                    # 刪除JSON和圖片文件
                    os.remove(json_path)
                    if os.path.exists(image_path):
                        os.remove(image_path)

    # 刪除沒有對應JSON文件的圖片
    if delete_img:
        for filename in os.listdir(source_folder):
            if filename.endswith('.jpg'):  # 根據實際情況修改圖片格式
                json_path = os.path.join(source_folder, filename.replace('.jpg', '.json'))
                if not os.path.exists(json_path):
                    image_path = os.path.join(source_folder, filename)
                    os.remove(image_path)
                    print(f"已刪除沒有對應JSON文件的圖片: {filename}")

    # 存儲已處理文件列表
    with open(processed_files_path, 'w') as f:
        json.dump(processed_files, f, indent=4)

    print("處理完成")