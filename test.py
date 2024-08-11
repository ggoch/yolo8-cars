from ultralytics import YOLO
from car_no.prosse_car_no_data import predict_event_img
from video_player import VideoPlayer
import video2img
import predict2labelme_json
import cv2
import tools.predict_folder_saveimg as predict_folder_saveimg
import split_data
import thing.predict_thing as predict
import thing.crop_lane_area as crop
import os
import json
import shutil
import pandas as pd
from thing.prosse_thing_data import random_copy_event_video,predict_event_video,predict_split_video_folder_by_id
from thing.create_split_video import create_video,copy_split_event_img_by_id

model_path = "models/wb/car_classV1.0/weights/best.pt"

model = YOLO(model_path)

results = model.predict("./四門.jpg", save=False)

img = results[0].plot()

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# # video_player = VideoPlayer("datas/videos/Barataria Morvant Exit.mp4")
# video_player = VideoPlayer("wbdatas/wb_videos/green/5.mp4")

# def predict(frame):
#     img = frame[:, :, ::-1].copy()  # 转换颜色空间
#     results = model.predict(img, save=False)
#     return results[0].plot()

# video_player.play(predict)

# video_path = "./wbdatas/wb_videos/white/8.mp4"

# video2img.toimg(video_path,"wb_08white")

# predict_folder_saveimg.predict_result_to_labelme_datas(model_path, "./wbdatas/split_output", "./datas/split_output_V8.0_result",conf=0.85)

# img = cv2.imread("./05b4cb1f-6f00-09fe-c9d9-3a0c65bc88eb_back00000084.jpg")

# crop_img = crop.crop_lane_area(img)

# result = predict.predict_thing_img(crop_img,model_path,conf=0.85,imgsz=640,return_img=True,save_path="./wbdatas/analyze")

# print(result)

# predict_event_img("./wbdatas/car_no_analyze/car_swipe_card","./models/license_car_noY8V3.pt","./wbdatas/car_no_analyze/car_swipe_card_result")

# random_copy_event_video("./wbdatas/test_output",250,"./wbdatas/analyze")
# random_copy_event_video("./wbdatas/test_output_2",250,"./wbdatas/analyze")

# random_copy_event_video("./wbdatas/analyze_true/back",222,"./wbdatas/analyze_true")
# random_copy_event_video("./wbdatas/analyze_true/front",278,"./wbdatas/analyze_true")


# predict_event_video("./wbdatas/analyze",model_path,"./wbdatas/analyze_result",False,conf=0.85,imgsz=640,e006_need_count=2)

# copy_split_event_img_by_id("./wbdatas/split_output","./wbdatas/analyze_true")

# create_video("./wbdatas/analyze_true/0a0c06bb-7111-50fd-b924-3a0ba1d286d4_back","./wbdatas/analyze_true.mp4",1)

# predict_split_video_folder_by_id("./wbdatas/analyze_true",model_path,"./wbdatas/analyze_true_result",True,conf=0.85,imgsz=640,e006_need_count=2)
