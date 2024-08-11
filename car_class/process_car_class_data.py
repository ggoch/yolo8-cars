import os
import random
import shutil
import pandas as pd
import cv2
import json
from car_class.predict import PredictCarClass

classMap = {
    "green": "事業廢棄物",
    "white": "回收車",
    "yellow": "一般垃圾車",
    "business_waste": "事業廢棄物",
    "recycling_truck": "一般垃圾車",
    "rubbish_truck": "回收車",
    "other": "其他",
}


def predict_event_img(folder_path, model_path, output_path):
    """
    預測指定資料夾中的所有車牌圖片，並將結果輸出成excel檔案
    """
    event_imgs = []
    predict_excel_datas = []

    result_folder_new_path = os.path.join(output_path, "result_img")

    if os.path.exists(result_folder_new_path) == False:
        os.makedirs(result_folder_new_path)

    predictCarClass = PredictCarClass(model_path, task="classify")

    for event in os.listdir(folder_path):
        event_path = os.path.join(folder_path, event)
        car_no = event.split(".")[0]
        event_imgs.append({"path": event_path, "car_no": car_no})

    for event in event_imgs:
        try:

            car_no = event["car_no"]
            event_path = event["path"]

            class_name = car_no.split("_")[1]

            class_name = classMap[class_name]

            result_text, img = predictCarClass.predict(cv2.imread(event_path))

            result_text = classMap[result_text] if result_text != None else "其他"

            print(f"事件 {os.path.basename(event_path)} 預測結果: {result_text}")

            save_path = os.path.join(result_folder_new_path, f"{car_no}.jpg")

            cv2.imwrite(save_path, img)

            predict_excel_datas.append(
                {
                    "檔名": car_no,
                    "類別": class_name,
                    "結果": result_text,
                    "是否正確": "正確" if class_name == result_text else "錯誤",
                    "偵測結果圖片位置": save_path,
                }
            )
        except Exception as e:
            print(f"Error processing event {event_path}: {e}")
            predict_excel_datas.append(
                {
                    "檔名": car_no,
                    "類別": class_name,
                    "結果": "Error",
                    "是否正確": "錯誤",
                    "偵測結果圖片位置": "無",
                }
            )

    predict_excel = pd.DataFrame(predict_excel_datas)

    predict_excel.to_excel(
        os.path.join(output_path, "predict_result.xlsx"), index=False
    )
    print(f"預測結果已輸出至 {os.path.join(output_path,'predict_result.xlsx')}")
