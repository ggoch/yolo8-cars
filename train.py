import os
import shutil
import time
from ultralytics import YOLO

def train_model(train_path,data_yaml_path,epochs=150,imgsz=640,batch_size=16,patience=100,lr0=0.01,lrf=0.1,model=None):

    if os.path.exists(train_path):
        shutil.rmtree(train_path)

    # model = YOLO("yolov8l.pt")
    if model is None:
        model = YOLO('yolov8n-seg.yaml').load('yolov8n.pt')  # build from YAML and transfer weights

    print("start training")
    t1 = time.time()
    model.train(
        imgsz=imgsz,
        epochs=epochs,
        data=data_yaml_path,
        batch=batch_size,
        patience=patience,
        lr0=0.01,
        lrf=0.1,
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
#     train_model("./runs/detect/train","./data.yaml",epochs=150)