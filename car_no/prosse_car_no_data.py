import os
import random
import shutil
import pandas as pd
import cv2
import json
from car_no.predict_car_no import PredictCarNo

def predict_event_img(folder_path,model_path,output_path):
    """
    預測指定資料夾中的所有車牌圖片，並將結果輸出成excel檔案
    """
    event_imgs = []
    predict_excel_datas = []

    result_folder_new_path = os.path.join(output_path, "result_img")

    if os.path.exists(result_folder_new_path) == False:
        os.makedirs(result_folder_new_path)

    predictCarNo = PredictCarNo(model_path,task="detect")
    
    for event in os.listdir(folder_path):
        event_path = os.path.join(folder_path, event)
        car_no = event.split(".")[0]
        event_imgs.append({
            "path":event_path,
            "car_no":car_no
        })
        
    for event in event_imgs:
        try:
            
            car_no = event["car_no"]
            event_path = event["path"]

            modified_car_no = car_no.replace("-", "")

            isSuccess,img,result_text = predictCarNo.detect(cv2.imread(event_path))

            print(f"事件 {os.path.basename(event_path)} 預測結果: {result_text}")

            save_path = os.path.join(result_folder_new_path, f"{car_no}.jpg")

            cv2.imwrite(save_path, img)

            predict_excel_datas.append({
                "車牌": car_no,
                "結果": result_text,
                "是否正確": True if modified_car_no == result_text else False,
                "偵測結果圖片位置":save_path if isSuccess else "無"
            })
        except Exception as e:
            print(f"Error processing event {event_path}: {e}")
            predict_excel_datas.append({
                "車牌": car_no,
                "結果": "Error",
                "是否正確": False,
                "偵測結果圖片位置":"無"
            })

    predict_excel = pd.DataFrame(predict_excel_datas)

    predict_excel.to_excel(os.path.join(output_path, "predict_result.xlsx"), index=False)
    print(f"已將預測結果保存到 {os.path.join(output_path, 'predict_result.xlsx')}")