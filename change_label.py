import label2coco

labelme_folder = "./datas"
export_dir = "./result"
label_txt = "label.txt"

# 創建轉換實例並執行轉換
label2coco.main(labelme_folder, export_dir,label_txt)