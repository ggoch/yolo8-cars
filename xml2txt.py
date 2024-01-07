import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse

path = "./datas/cars/annotations"
classes = {"licence": 0}
labels_path = "./datas/cars/polygon-labels"

if not os.path.exists(labels_path):
    os.mkdir(labels_path)

# train_path=os.path.join(labels_path,"licence")
train_path = labels_path

if not os.path.exists(train_path):
    os.mkdir(train_path)

def convert_to_polygon(x_center, y_center, width, height):
    # """從中心點和寬高轉換為多邊形的四個頂點。"""
    x_center, y_center, width, height = map(float, [x_center, y_center, width, height])
    
    # 計算矩形的四個角點
    x1 = x_center - width / 2
    y1 = y_center - height / 2
    x2 = x_center + width / 2
    y2 = y_center - height / 2
    x3 = x_center + width / 2
    y3 = y_center + height / 2
    x4 = x_center - width / 2
    y4 = y_center + height / 2

    return [x1, y1, x2, y2, x3, y3, x4, y4]

for annotations in os.listdir(path):
    dom = parse(os.path.join(path, annotations))
    root = dom.documentElement
    filename = ".txt".join(root.getElementsByTagName("filename")[0].childNodes[0].data.split(".png"))
    image_width = root.getElementsByTagName("width")[0].childNodes[0].data
    image_height = root.getElementsByTagName("height")[0].childNodes[0].data

    with open("./datas/cars/polygon-labels/" + filename, "w") as r:
        for items in root.getElementsByTagName("object"):
            name = items.getElementsByTagName("name")[0].childNodes[0].data
            xmin = items.getElementsByTagName("xmin")[0].childNodes[0].data
            ymin = items.getElementsByTagName("ymin")[0].childNodes[0].data
            xmax = items.getElementsByTagName("xmax")[0].childNodes[0].data
            ymax = items.getElementsByTagName("ymax")[0].childNodes[0].data
            x_center_norm = ((int(xmin) + int(xmax)) / 2) / int(image_width)
            y_center_norm = ((int(ymin) + int(ymax)) / 2) / int(image_height)
            width_norm = ((int(xmax) - int(xmin)) / int(image_width))
            height_norm = ((int(ymax) - int(ymin)) / int(image_height))

            # 轉換為多邊形的四個頂點
            polygon = convert_to_polygon(x_center_norm, y_center_norm, width_norm, height_norm)
            r.write(str(classes[name]) + " ")
            r.write(" ".join([str(a) for a in polygon]) + "\n")
            
            

# for annotations in os.listdir(path):
#     dom = parse(os.path.join(path, annotations))
#     root = dom.documentElement
#     filename = ".txt".join(root.getElementsByTagName("filename")[0].childNodes[0].data.split(".png"))
#     image_width = root.getElementsByTagName("width")[0].childNodes[0].data
#     image_height = root.getElementsByTagName("height")[0].childNodes[0].data

#     with open("./datas/cars/labels/" + filename, "w") as r:
#         for items in root.getElementsByTagName("object"):
#             name = items.getElementsByTagName("name")[0].childNodes[0].data
#             xmin = items.getElementsByTagName("xmin")[0].childNodes[0].data
#             ymin = items.getElementsByTagName("ymin")[0].childNodes[0].data
#             xmax = items.getElementsByTagName("xmax")[0].childNodes[0].data
#             ymax = items.getElementsByTagName("ymax")[0].childNodes[0].data
#             x_center_norm = ((int(xmin) + int(xmax)) / 2) / int(image_width)
#             y_center_norm = ((int(ymin) + int(ymax)) / 2) / int(image_height)
#             width_norm = ((int(xmax) - int(xmin)) / int(image_width))
#             height_norm = ((int(ymax) - int(ymin)) / int(image_height))
#             r.write(str(classes[name]) + " ")
#             r.write(str(x_center_norm) + " ")
#             r.write(str(y_center_norm) + " ")
#             r.write(str(width_norm) + " ")
#             r.write(str(height_norm) + "\n")
            
