import os
import platform
import pylab as plt
import cv2
import numpy as np
import pytesseract
import time

from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

from collections import defaultdict

import show_fn


model = YOLO("models/first-train/weights/best.pt")  # load a custom model
path = "datas/valid/images"
plt.figure(figsize=(10, 10))

cap = cv2.VideoCapture("datas/videos/Barataria Morvant Exit.mp4")

startTime = time.time()
frameCount = 0

# Store the track history
track_history = defaultdict(lambda: [])

# for i, f in enumerate(os.listdir(path)[0:6]):
#     full = os.path.join(path, f)
#     print(full)

#     img = cv2.imdecode(np.fromfile(full, dtype=np.uint8), cv2.IMREAD_COLOR)
#     img = img[:, :, ::-1].copy()

#     results = model.predict(img, save=False)
#     boxes = results[0].boxes.xyxy

#     for box in boxes:
#         # box=box.cpu().numpy()
#         x1 = int(box[0])
#         y1 = int(box[1])
#         x2 = int(box[2])
#         y2 = int(box[3])
#         img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

#         tmp = cv2.cvtColor(img[y1:y2, x1:x2].copy(), cv2.COLOR_BGR2GRAY)
#         license = pytesseract.image_to_string(tmp, lang="eng", config="--psm 11")
#         img = text(img, license, (x1, y1 - 20), (255, 0, 0), 30)

#     plt.subplot(2, 3, i + 1)
#     plt.axis("off")
#     plt.imshow(img)

# plt.savefig("yolov8_car.jpg")
# plt.show()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


    frameCount += 1

    # # 處理每一幀（以下代碼與處理單張圖片相同）
    img = frame[:, :, ::-1].copy()  # 轉換顏色空間
    results = model.predict(img, save=False)
    # results = model.track(img, conf=0.3, iou=0.5,persist=True)
    boxes = results[0].boxes.xyxy

    # boxes = results[0].boxes.xywh.cpu()
    # track_ids = results[0].boxes.id.int().cpu().tolist()

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    for box in boxes:
        x1, y1, x2, y2 = map(int, box[:4])
        # img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        gray_img = annotated_frame[y1:y2, x1:x2].copy()
        print(gray_img)
        tmp = cv2.cvtColor(gray_img, cv2.COLOR_BGR2GRAY)
        license = pytesseract.image_to_string(tmp, lang='eng', config='--psm 11')
        annotated_frame = show_fn.drow_text(annotated_frame, license, (x1, y1 - 20), (255, 0, 0), 30)

    annotated_frame = show_fn.get_fps(annotated_frame, startTime, frameCount)

    # # 顯示結果
    cv2.imshow('YOLO + OCR', cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))

    # Plot the tracks
    # for box, track_id in zip(boxes, track_ids):
    #     x, y, w, h = box
    #     track = track_history[track_id]
    #     track.append((float(x), float(y)))  # x, y center point
    #     if len(track) > 30:  # retain 90 tracks for 90 frames
    #         track.pop(0)

    #     # Draw the tracking lines
    #     points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
    #     cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

    # Display the annotated frame
    # cv2.imshow("YOLOv8 Tracking", annotated_frame)

    # 按 'q' 鍵退出循環
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 釋放視頻捕獲對象
cap.release()
cv2.destroyAllWindows()
