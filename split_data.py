import os
import random
import shutil

data_path = "./datas/cars"
train_path = "./datas/test/train"
valid_path = "./datas/test/valid"

img_source_dir = "images"
label_source_dir = "labels"

img_target_dir = "images"
label_target_dir = "labels"

def split(data_path,train_path,valid_path,img_source_dir="images",label_source_dir="labels",img_target_dir="images",label_target_dir="labels",split_ratio=0.8):
    '''
    data_path: the path of the data
    train_path: the path of the train data
    valid_path: the path of the valid data
    img_source_dir: the name of the image folder in the data_path
    label_source_dir: the name of the label folder in the data_path
    img_target_dir: the name of the image folder in the train_path and valid_path
    label_target_dir: the name of the label folder in the train_path and valid_path
    split_ratio: the ratio of the train data and valid data    
    '''
    if os.path.exists(train_path):
        shutil.rmtree(train_path)

    if os.path.exists(valid_path):
        shutil.rmtree(valid_path)

    os.makedirs(os.path.join(train_path, img_source_dir))
    os.makedirs(os.path.join(train_path, label_source_dir))
    os.makedirs(os.path.join(valid_path, img_target_dir))
    os.makedirs(os.path.join(valid_path, label_target_dir))

    files = [
        os.path.splitext(file)[0] for file in os.listdir(os.path.join(data_path, img_source_dir))
    ]

    random.shuffle(files)
    mid = int(len(files) * split_ratio)

    for file in files[:mid]:
        source = os.path.join(data_path, img_source_dir, f"{file}.png")
        target = os.path.join(train_path, img_target_dir, f"{file}.png")
        print(source, target)
        shutil.copy(source, target)

        source = os.path.join(data_path, label_source_dir, f"{file}.txt")
        target = os.path.join(train_path, label_target_dir, f"{file}.txt")
        print(source, target)
        shutil.copy(source, target)

    for file in files[mid:]:
        source = os.path.join(data_path, img_source_dir, f"{file}.png")
        target = os.path.join(valid_path, img_target_dir, f"{file}.png")
        print(source, target)
        shutil.copy(source, target)

        source = os.path.join(data_path, label_source_dir, f"{file}.txt")
        target = os.path.join(valid_path, label_target_dir, f"{file}.txt")
        print(source, target)
        shutil.copy(source, target)

    print("done")

# split(data_path,train_path,valid_path,img_source_dir,label_source_dir,img_target_dir,label_target_dir,split_ratio=0.8)