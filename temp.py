import split_data
from xml2txt import xml2txt

# path = "./datas/labels/PascalVoc"
# output_path = "./datas/labels/Labels"

# classes = {
#     "license plate": 0,
#     "1": 1,
#     "2": 2,
#     "3": 3,
#     "4": 4,
#     "5": 5,
#     "6": 6,
#     "7": 7,
#     "8": 8,
#     "9": 9,
#     "0": 10,
#     "A": 11,
#     "B": 12,
#     "C": 13,
#     "D": 14,
#     "E": 15,
#     "F": 16,
#     "G": 17,
#     "H": 18,
#     "I": 19,
#     "J": 20,
#     "K": 21,
#     "L": 22,
#     "M": 23,
#     "N": 24,
#     "O": 25,
#     "P": 26,
#     "Q": 27,
#     "R": 28,
#     "S": 29,
#     "T": 30,
#     "U": 31,
#     "V": 32,
#     "W": 33,
#     "X": 34,
#     "Y": 35,
#     "Z": 36,
#     }

# xml2txt(path, output_path, classes,img_type=".jpg")

# 將資料切分成訓練集合驗證集

img_source_dir = "image"
label_source_dir = "Labels"

data_path = "./datas/labels_test"
train_path = "./datas/training/train/base"
valid_path = "./datas/training/valid/base"

split_data.split(data_path,train_path,valid_path,img_source_dir,label_source_dir)