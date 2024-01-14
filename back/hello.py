from ultralytics import YOLO
from PIL import Image

# # Load a model
# model = YOLO('yolov8n.yaml')  # build a new model from YAML
# model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
# model = YOLO('yolov8n.yaml').load('yolov8n.pt')  # build from YAML and transfer weights

# # Train the model
# results = model.train(data='coco128.yaml', epochs=100, imgsz=640)

# model = YOLO('runs/detect/train/weights/last.pt')  # create

# results = model.train(resume=True)

# Load a model
# if __name__ == "__main__":
#     model = YOLO('yolov8n.pt')  # load an official model
#     model = YOLO('runs/detect/train/weights/best.pt')  # load a custom model
    
#     # Validate the model
#     metrics = model.val()  # no arguments needed, dataset and settings remembered
#     metrics.box.map    # map50-95
#     metrics.box.map50  # map50
#     metrics.box.map75  # map75
#     metrics.box.maps 

# model = YOLO('yolov8n.pt')  # pretrained YOLOv8n model
# model = YOLO('runs/detect/train/weights/best.pt')  # load a custom model
model = YOLO('runs/segment/train3/weights/best.pt')  # load a custom model
# model = YOLO('yolov8n-seg.yaml').load('yolov8n.pt')  # build from YAML and transfer weights

# Train the model
# if __name__ == '__main__':
#     results = model.train(data='coco128-seg.yaml', epochs=100, imgsz=640)

# Run batched inference on a list of images
# results = model(['datas/img1.jpg', 'datas/img2.jpg'])  # return a list of Results objects
results = model(['datas/Cars3.png'])  # return a list of Results objects

# Process results list
for result in results:
    # boxes = result.boxes  # Boxes object for bbox outputs
    # masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    # probs = result.probs  # Probs object for classification outputs
    print(len(result.masks))
    print(len(result.boxes))
    im_array = result.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    # im.save(f'{result}.jpg')  # save image