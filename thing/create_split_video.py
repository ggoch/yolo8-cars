import cv2
import os
import re
import shutil

def create_video(image_folder, output_video, fps=30):
    """
    將圖片文件夾中的所有圖片合併成一個影片
    """
    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()  # 確保圖片按順序排列

    if len(images) == 0:
        print("No images found in the folder.")
        return

    # 讀取第一張圖片以獲取尺寸
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # 定義視頻編碼和輸出文件
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    video.release()
    print(f"Video saved as {output_video}")

def get_split_filename(filename):
    # 移除文件擴展名
    name_without_ext = filename.split('.')[0]

    # 使用正則表達式來拆分文件名
    match = re.match(r"([a-f0-9\-]+)_([a-z]+)(\d+)", name_without_ext)
    if match:
        part1 = match.group(1)
        part2 = match.group(2)
        part3 = match.group(3)
        return part1, part2, part3
    else:
        raise ValueError("Filename format does not match expected pattern.")
    
def copy_split_event_img_by_id(folder_path,output_path):
    """
    將指定資料夾中的所有事件影像按照ID分類複製到不同的資料夾中
    """
    def copy_cache_img(img_cache_list):
        sorted_img_cache_list = sorted(img_cache_list, key=lambda x: x["ret"])
        for img_cache in sorted_img_cache_list:
            event_folder_path = os.path.join(output_path, f'{img_cache["event_id"]}_{img_cache["position"]}')

            if os.path.exists(event_folder_path) == False:
                os.makedirs(event_folder_path)

            shutil.copy(os.path.join(folder_path, img_cache["img"]), os.path.join(event_folder_path, img_cache["img"]))

    split_img_datas = []

    for img in os.listdir(folder_path):
        event_id, position, ret = get_split_filename(img)

        split_img_datas.append({
            "event_id": event_id,
            "position": position,
            "ret": ret,
            "img": img
        })

    sorted_split_img_datas = sorted(split_img_datas, key=lambda x: x["event_id"])

    img_cache_list = []

    for split_img_data in sorted_split_img_datas:
        event_id = split_img_data["event_id"]
        position = split_img_data["position"]
        img = split_img_data["img"]

        if len(img_cache_list) == 0:
            img_cache_list.append(split_img_data)
            continue
        elif img_cache_list[-1]["event_id"] != event_id:
            copy_cache_img(img_cache_list)
            img_cache_list = []
        elif img_cache_list[-1]["position"] != position:
            copy_cache_img(img_cache_list)
            img_cache_list = []
        

        img_cache_list.append(split_img_data)

# if __name__ == "__main__":
#     image_folder = "path/to/your/image_folder"  # 圖片文件夾路徑
#     output_video = "output_video.mp4"           # 輸出視頻文件名
#     fps = 30  # 每秒幀數（根據需要調整）

#     create_video(image_folder, output_video, fps)