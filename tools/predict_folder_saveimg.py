from ultralytics import YOLO
from PIL import Image
import os
import os.path as osp
import base64
import json
import glob
import shutil
import sys
from enum import Enum
import cv2

class imageType(Enum):
    JPG = 1
    PNG = 2

def predict_result_to_labelme_datas(model_path, input_dir, output_dir,image_type=imageType.JPG,conf=0.25,imgsz=640):
    if osp.exists(output_dir):
        print("Output directory already exists:", output_dir)
        sys.exit(1)
    os.makedirs(output_dir)

    image_files = None

    if image_type == imageType.JPG:
        image_files = glob.glob(osp.join(input_dir, "*.jpg"))
    elif image_type == imageType.PNG:
        image_files = glob.glob(osp.join(input_dir, "*.png"))

    model = YOLO(model_path)  # load a custom model

    for image_id, image_file in enumerate(image_files):
        try:
            results = model.predict(image_file,conf=conf,imgsz=imgsz)
            base = osp.splitext(osp.basename(image_file))[0]

            destination = osp.join(output_dir, f"{base}.jpg")

            result = results[0]
            if result.masks is None:
                print(f"Skip image {image_file}")
                continue

            # 保存圖片
            cv2.imwrite(destination, results[0].plot())
            print(f"Saved image to {destination}")

        except Exception as e:
            print(f"Error processing image {image_file}: {e}")

    print("Done")