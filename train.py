import os
import shutil
import time
from ultralytics import YOLO

def train_model(train_path,data_yaml_path,epochs=150,imgsz=640,batch_size=16,patience=100,lr0=0.01,lrf=0.1):

    if os.path.exists(train_path):
        shutil.rmtree(train_path)

    # model = YOLO("yolov8n-cls.pt")
    model = YOLO("yolov8n.pt")
    # model = YOLO('yolov8n-seg.yaml').load('yolov8n.pt')  # build from YAML and transfer weights

    print("start training")
    t1 = time.time()
    model.train(
        imgsz=imgsz,
        epochs=epochs,
        data=data_yaml_path,
        # data="caltech256",
        batch=10,
        patience=patience,
        lr0=0.01,
        lrf=0.1,
        # task="classify",
        # weights="yolov8l.pt",
        # project="runs/detect",
        # name="train",
        # exist_ok=True,
    )

    t2 = time.time()
    print(f"training time : {t2-t1} seconds")

    path = model.export()
    print(f"model export path : {path}")

# if __name__ == "__main__":
#     # yaml裡面的data路徑從datasets開始
#     # train_model("./runs/detect/train","C:/Users/ggoch2/Desktop/Yolov8/data_car_class.yaml",epochs=300)
#     train_model("./runs/detect/train","./datasets/custom",epochs=300)