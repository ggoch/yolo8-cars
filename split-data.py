import os
import random
import shutil

data_path = "./datas/cars"
train_path = "./datas/train"
valid_path = "./datas/valid"

img_source_dir = "images"
label_source_dir = "polygon-labels"

img_target_dir = "images"
label_target_dir = "polygon-labels"

if os.path.exists(train_path):
    shutil.rmtree(train_path)

if os.path.exists(valid_path):
    shutil.rmtree(valid_path)

os.makedirs(os.path.join(train_path, img_source_dir))
os.makedirs(os.path.join(train_path, label_source_dir))
os.makedirs(os.path.join(valid_path, img_target_dir))
os.makedirs(os.path.join(valid_path, label_target_dir))

files = [
    os.path.splitext(file)[0] for file in os.listdir(os.path.join(data_path, "images"))
]
random.shuffle(files)
mid = int(len(files) * 0.8)

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