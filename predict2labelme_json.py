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

class imageType(Enum):
    JPG = 1
    PNG = 2

def predict_result_to_labelme_datas(model_path, input_dir, output_dir,image_type=imageType.JPG):
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
        results = model.predict(image_file)
        base = osp.splitext(osp.basename(image_file))[0]

        destination = osp.join(output_dir, f"{base}.jpg")
        shutil.copy(image_file, destination)

        result = results[0]

        shapes = []

        if result.masks is None:
            continue

        for i, mask in enumerate(result.masks):
            yolojson_str = result.tojson()
            yolojson = json.loads(yolojson_str)
            yolojson = yolojson[i]

            x_coords = yolojson["segments"]["x"]
            y_coords = yolojson["segments"]["y"]

            points = [[x, y] for x, y in zip(x_coords, y_coords)]

            shape_dict = {
                "label": yolojson["name"],  # 这里需要指定标签
                "points": points,
                "group_id": None,
                "description": "",
                "shape_type": "polygon",
                "flags": {},
            }
            shapes.append(shape_dict)

        with open(image_file, "rb") as image_file:
            # 将图像转换为 Base64 编码
            encoded_string = base64.b64encode(image_file.read()).decode()

        json_data = {
            "version": "5.3.0",
            "flags": {},
            "shapes": shapes,
            "imagePath": osp.basename(result.path),  # 指定图像路径
            "imageData": encoded_string,  # 需要提供 Base64 编码的图像数据
            "imageHeight": result.orig_shape[0],
            "imageWidth": result.orig_shape[1],
        }

        with open(osp.join(output_dir, f"{base}.json"), "w") as f:
            json.dump(json_data, f, indent=4)


predict_result_to_labelme_datas(
    "models/segment/weights/best.pt", "videos/Barataria Morvant Exit", "dataset/train/images"
)
