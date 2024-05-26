from ultralytics import YOLO
from video_player import VideoPlayer
import video2img
import predict2labelme_json
import cv2
import tools.predict_folder_saveimg as predict_folder_saveimg

model_path = "models/wb/thingV8.0/weights/best.pt"

# model = YOLO(model_path)

# # video_player = VideoPlayer("datas/videos/Barataria Morvant Exit.mp4")
# video_player = VideoPlayer("wbdatas/wb_videos/green/5.mp4")

# def predict(frame):
#     img = frame[:, :, ::-1].copy()  # 转换颜色空间
#     results = model.predict(img, save=False)
#     return results[0].plot()

# video_player.play(predict)

# video_path = "./wbdatas/wb_videos/white/8.mp4"

# video2img.toimg(video_path,"wb_08white")

predict_folder_saveimg.predict_result_to_labelme_datas(model_path, "./wbdatas/split_output", "./datas/split_output_V8.0_result",conf=0.85)