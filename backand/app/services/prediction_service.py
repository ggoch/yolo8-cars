from PIL import Image
import numpy as np
import io

def prepare_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    return image

def predict(image, model,conf=0.25,imgsz=640):
    result = model.predict(image,save=False,conf=conf,imgsz=imgsz)
    return result[0].plot()