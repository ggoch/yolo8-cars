from ultralytics import YOLO
import json
import thing.crop_lane_area as crop
from tools.box_is_inside import box_is_inside
import cv2
import os

def predict_thing_img(img,model_path,conf=0.25,imgsz=640,e006_need_count=2,return_img=False,save_path=None):
    """
    預測指定影像中的物件，並判斷是否有指定數量的E006

    return_img: 是否保存偵測到目標的圖像
    save_path: 保存圖像的路徑
    """
    model = YOLO(model_path)

    save_path = os.path.join(save_path,"predict_thing_img.jpg") if save_path is not None else "predict_thing_img.jpg"

    try:
        results = model.predict(img,conf=conf,imgsz=imgsz)

        result = results[0]

        if result.masks is None:
            print(f"Not find any thing in image")
            return False
        
        area = None
        label_datas = []
        find_e006_count = 0
        
        for i, mask in enumerate(result.masks):
            yolojson_str = result.tojson()
            yolojson = json.loads(yolojson_str)
            yolojson = yolojson[i]

            boxs = yolojson["box"]
            label = yolojson["name"]
            conf = yolojson["confidence"]

            if label == "garbage area":
                if area is not None and area["conf"] < conf:
                    area = {
                        "label": label,
                        "boxs":boxs,
                        "conf":conf
                    }
                    return False
                else:
                    area = {
                        "label": label,
                        "boxs":boxs,
                        "conf":conf
                    }
                continue



            label_datas.append({
                "label": label,
                "boxs":boxs
            })

        if len(label_datas) == 0 or area is None:
            print(f"Not find any thing in image")
            return False
        
        for label_data in label_datas:
            if box_is_inside(label_data["boxs"],area["boxs"]):
                print(f"Find {label_data['label']} in image")
                find_e006_count += 1

            if find_e006_count >= e006_need_count:
                print(f"Find {e006_need_count} e006 in image")
                
                if return_img:
                    cv2.imwrite(save_path,img)
                return True   
    except Exception as e:
        print(f"Error processing image {img}: {e}")
        return None
    
def predict_thing_video(video_path,model_path,conf=0.25,imgsz=640,e006_need_count=2,return_img=False,save_path=None):
    video = cv2.VideoCapture(video_path)

    while True:
        ret, frame = video.read()

        if not ret:
            return False
        
        crop_img = crop.crop_lane_area(frame)

        result = predict_thing_img(crop_img,model_path,conf=conf,imgsz=imgsz,e006_need_count=e006_need_count,return_img=return_img,save_path=save_path)

        if result == True:
            return True
                