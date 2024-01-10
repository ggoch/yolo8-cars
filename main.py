import xml2txt
import split_data
import train
import show_fn

from ultralytics import YOLO
import cv2
import time


path = "./datas/cars/annotations"
labels_path = "./datas/cars/labels"

xml2txt.xml2txt(path, labels_path)

data_path = "./datas/cars"
train_path = "./datas/test/train"
valid_path = "./datas/test/valid"

split_data.split(data_path,train_path,valid_path)

if __name__ == "__main__":
    # yaml裡面的data路徑從datasets開始
    train.train_model("./runs/detect/train","./data.yaml",epochs=150)

model = YOLO("./runs/detect/train/weights/best.pt")

cap = cv2.VideoCapture("datas/videos/Barataria Morvant Exit.mp4")

startTime = time.time()
frameCount = 0
skipFrameCount = 30

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


    frameCount += 1

    if frameCount % skipFrameCount == 0:
        # # 處理每一幀（以下代碼與處理單張圖片相同）
        img = frame[:, :, ::-1].copy()  # 轉換顏色空間
        results = model.predict(img, save=False)
        # results = model.track(img, conf=0.3, iou=0.5,persist=True)
        
        annotated_frame = results[0].plot()

    annotated_frame = show_fn.get_fps(annotated_frame, startTime, frameCount)

    # # 顯示結果
    cv2.imshow('YOLO', cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))

    # 按 'q' 鍵退出循環
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 釋放視頻捕獲對象
cap.release()
cv2.destroyAllWindows()