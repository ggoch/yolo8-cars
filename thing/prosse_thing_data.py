import os
import random
import shutil
import pandas as pd
import cv2
import json
from thing.crop_lane_area import crop_lane_area
from thing.predict_thing import predict_thing_video,predict_thing_img


def random_copy_event_video(folder_path,count,output_folder_path):
    """
    隨機從指定資料夾中複製指定數量的事件資料夾到指定資料夾中
    """
    event_paths = []
    
    for event in os.listdir(folder_path):
        event_path = os.path.join(folder_path, event)
        if os.path.isdir(event_path):
            event_paths.append(event_path)
        
    random_event_paths = random.sample(event_paths, count)

    for event_path in random_event_paths:
        event_name = os.path.basename(event_path)
        output_event_path = os.path.join(output_folder_path, event_name)
            
        shutil.copytree(event_path, output_event_path)
        print(f"已將事件 {event_name} 複製到 {output_event_path}")
    
    return random_event_paths

def predict_event_video(folder_path,model_path,output_path,correct,conf=0.25,imgsz=640,e006_need_count=2):
    """
    預測指定資料夾中的所有事件影像，並將結果輸出成excel檔案
    """
    event_video_paths = []
    predict_excel_datas = []

    original_folder_new_path = os.path.join(output_path, "original")
    
    for event in os.listdir(folder_path):
        event_path = os.path.join(folder_path, event)
        if os.path.isdir(event_path):
            event_video_paths.append(event_path)
        
    for event_path in event_video_paths:
        try:
            base_name = os.path.basename(event_path)
            event_id = base_name.split("_")[0]
            position = base_name.split("_")[1]

            event_path = os.path.join(event_path, "result.mp4")

            original_folder_new_event_path = os.path.join(original_folder_new_path, base_name)

            if os.path.exists(original_folder_new_event_path) == False:
                os.makedirs(original_folder_new_event_path)

            result = predict_thing_video(event_path,model_path,conf,imgsz,e006_need_count,return_img=True,save_path=original_folder_new_event_path)

            print(f"事件 {os.path.basename(event_path)} 預測結果: {result}")

            shutil.copy(event_path, original_folder_new_event_path)

            predict_excel_datas.append({
                "Id": event_id,
                "前/後": "前" if "front" in position else "後",
                "結果": result,
                "正確答案": correct,
                "是否正確": True if result == correct else False,
                "原始檔案位置":os.path.join(original_folder_new_event_path, "result.mp4"),
                "偵測成功圖片位置":os.path.join(original_folder_new_event_path, "predict_thing_img.jpg") if result else "無"
            })
        except Exception as e:
            print(f"Error processing event {event_path}: {e}")
            predict_excel_datas.append({
                "Id": event_id,
                "前/後": "前" if "front" in position else "後",
                "結果": "Error",
                "正確答案": correct,
                "是否正確": False,
                "原始檔案位置":"無",
                "偵測成功圖片位置":"無"
            })

    predict_excel = pd.DataFrame(predict_excel_datas)

    predict_excel.to_excel(os.path.join(output_path, "predict_result.xlsx"), index=False)
    print(f"已將預測結果保存到 {os.path.join(output_path, 'predict_result.xlsx')}")

def predict_split_video_folder(folder_path,model_path,conf=0.25,imgsz=640,e006_need_count=2):
    """
    預測指定資料夾中的所有事件圖片，需先切成每幀圖片的格式，判斷是否有指定數量的e006，並返回結果
    """
        
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)
        crop_img = crop_lane_area(img)
        result = predict_thing_img(crop_img,model_path,conf,imgsz,e006_need_count,return_img=True,save_path=folder_path)

        if result:
            return True
    
    return False

def predict_split_video_folder_by_id(folder_path,model_path,output_path,correct,conf=0.25,imgsz=640,e006_need_count=2):
    predict_excel_datas = []

    original_folder_new_path = os.path.join(output_path, "original")

    for event in os.listdir(folder_path):
        event_path = os.path.join(folder_path, event)
        if os.path.isdir(event_path):
            try:
                result = predict_split_video_folder(event_path,model_path,conf,imgsz,e006_need_count)

                base_name = os.path.basename(event)
                event_id = base_name.split("_")[0]
                position = base_name.split("_")[1]

                original_folder_new_event_path = os.path.join(original_folder_new_path, base_name)

                shutil.copytree(event_path, original_folder_new_event_path)
                print(f"已將事件 {event} 複製到 {original_folder_new_event_path}")

                predict_excel_datas.append({
                    "Id": event_id,
                    "前/後": "前" if "front" in position else "後",
                    "結果": result,
                    "正確答案": correct,
                    "是否正確": True if result == correct else False,
                    "原始檔案位置":event_path,
                    "偵測成功圖片位置":os.path.join(original_folder_new_event_path, "predict_thing_img.jpg")
                })
            except Exception as e:
                print(f"Error processing event {event_path}: {e}")
                predict_excel_datas.append({
                    "Id": event_id,
                    "前/後": "前" if "front" in position else "後",
                    "結果": "Error",
                    "正確答案": correct,
                    "是否正確": False,
                    "原始檔案位置":event_path,
                    "偵測成功圖片位置":"無"
                })

    predict_excel = pd.DataFrame(predict_excel_datas)
    predict_excel.to_excel(os.path.join(output_path, "predict_result.xlsx"), index=False)
    print(f"已將預測結果保存到 {os.path.join(output_path, 'predict_result.xlsx')}")
    
