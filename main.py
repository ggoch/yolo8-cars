import xml2txt
import split_data
import train
import show_fn

from ultralytics import YOLO
import cv2
import time


# path = "./datas/cars/annotations"
# labels_path = "./datas/cars/labels"

# xml2txt.xml2txt(path, labels_path)

# data_path = "./datas/cars"
# train_path = "./datas/test/train"
# valid_path = "./datas/test/valid"

# split_data.split(data_path,train_path,valid_path)

# if __name__ == "__main__":
#     # yaml裡面的data路徑從datasets開始
#     train.train_model("./runs/detect/train","./data.yaml",epochs=150)

# model = YOLO("./runs/detect/train/weights/best.pt")
model = YOLO("models/first-train/weights/best.pt")  # load a custom model

cap = cv2.VideoCapture("datas/videos/Barataria Morvant Exit.mp4")

startTime = time.time()
frameCount = 0
skipFrameCount = 10
paused = False  # 暂停标志
fast_forward_frame_count = 30
rewind_frame_count = 30

# 在循环外初始化结果存储变量
last_results = None

while cap.isOpened():
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break

        annotated_frame = frame.copy() 
        
        frameCount += 1

        annotated_frame = None

        if frameCount % skipFrameCount == 0:
            img = frame[:, :, ::-1].copy()  # 转换颜色空间
            results = model.predict(img, save=False)

            # 保存预测结果供后续帧使用
            last_results = results
            annotated_frame = results[0].plot()
        else:
            # 如果有最后的预测结果，绘制它们
            if last_results is not None:
                annotated_frame = last_results[0].plot()
            else:
                annotated_frame = frame[:, :, ::-1].copy()

        # 在每一帧都重新计算并绘制FPS
        annotated_frame = show_fn.get_fps(annotated_frame, startTime, frameCount)

        # # 顯示結果
        cv2.imshow('YOLO', cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))


    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("k"):  # 暂停/播放
        paused = not paused
    elif key == ord("j") and frameCount > 1:  # 倒退一帧
        # 计算新的帧数，不能小于0
        frameCount = max(0, frameCount - rewind_frame_count)
        # 设置视频的当前帧位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameCount)
    elif key == ord("l"):  # 前进一帧
        # 计算新的帧数，不能超过视频的总帧数
        frameCount = min(cap.get(cv2.CAP_PROP_FRAME_COUNT), frameCount + fast_forward_frame_count)
        # 设置视频的当前帧位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameCount)

    # 如果我们处于暂停状态并且没有按键操作，就在这里等待
    while paused:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("k"):  # 再次按 'k' 继续播放
            paused = False
            break
        elif key == ord("q"):  # 退出
            break
        time.sleep(0.1)  # 减少循环速度，以防止高CPU占用

    if paused:  # 如果退出暂停循环是因为按了退出键，那么也应该退出外层循环
        break

# 釋放視頻捕獲對象
cap.release()
cv2.destroyAllWindows()