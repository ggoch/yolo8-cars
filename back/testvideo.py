from video_player import VideoPlayer
from ultralytics import YOLO

model = YOLO("models/first-train/weights/best.pt")

video_player = VideoPlayer("datas/videos/Barataria Morvant Exit.mp4")

def predict(frame):
    img = frame[:, :, ::-1].copy()  # 转换颜色空间
    results = model.predict(img, save=False)
    return results[0].plot()

video_player.play(predict)