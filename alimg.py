import albumentations as A
import cv2
import numpy as np
import matplotlib.pyplot as plt
import transforms as T
import os
import os.path as osp
import sys
import tool as tool

def plot_image_anns(image, masks):
    num_masks = len(masks)
    plt.figure(figsize=(12, 2 * num_masks))  # 调整图像大小

    # 顯示變換後的圖像
    plt.subplot(num_masks + 1, 2, 1) 
    plt.imshow(image)
    plt.title('Transformed Image')
    plt.axis('off')

    # 顯示變換後的掩碼
    for i, mask in enumerate(masks):
        plt.subplot(num_masks + 1, 2, 2 + i * 2)  # 每个 mask 占据一行
        plt.imshow(mask, cmap='gray')  # 使用灰度颜色映射
        plt.title(f'Transformed Mask {i+1}')
        plt.axis('off')

    plt.tight_layout()
    plt.show()

def masks_to_polygons_with_id(masks, class_ids,closed=True):
    polygons = []
    for i, mask in enumerate(masks):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            contour = cv2.approxPolyDP(contour, 3, True)
            # 生成多边形字符串，包含类别 ID 和索引
            polygon_str = f"{class_ids[i]} " + " ".join(f"{point[0][0]:.2f} {point[0][1]:.2f}" for point in contour)
            polygons.append(polygon_str)
    return polygons

def polygons_to_masks_with_id(polygons, height, width):
    masks = np.zeros((len(polygons), height, width), dtype=np.uint8)
    class_ids = []
    for i, polygon_str in enumerate(polygons):
        parts = polygon_str.split()
        class_id = int(parts[0])  # 提取 ClassId
        class_ids.append(class_id)

        polygon = [int(float(num)) for num in parts[1:]]
        points = [(polygon[j], polygon[j+1]) for j in range(0, len(polygon), 2)]
        cv2.fillPoly(masks[i, :, :], [np.array(points, dtype=np.int32)], 1)

    return masks, class_ids

def read_polygons_from_file(file_path):
    with open(file_path, 'r') as file:
        polygons = file.readlines()
    # 移除換行符號並返回
    return [line.strip() for line in polygons]

def transform_image_label(image_dir, label_dir,output_dir):
    transform = T.Transforms()

    tool.check_output_dir_already_exists(output_dir)
    os.makedirs(osp.join(output_dir, "JPEGImages"))
    os.makedirs(osp.join(output_dir, "Labels"))

    image_files = tool.read_image_dir(image_dir,tool.imageType.JPG)

    print("Transforming images and labels...")

    for image_id, image_file in enumerate(image_files):
        image = cv2.imread(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width = image.shape[:2]

        base = osp.splitext(osp.basename(image_file))[0]

        label_file = osp.join(label_dir, f"{base}.txt")

        polygons = read_polygons_from_file(label_file)

        masks, class_ids = polygons_to_masks_with_id(polygons, height, width)

        image,masks = transform.random(image=image, masks=masks)

        # 顯示變換後的圖像和掩碼
        # plot_image_anns(image, masks)

        polygons = masks_to_polygons_with_id(masks, class_ids, closed=False)

        with open(osp.join(output_dir,"Labels", f"{base}.txt"), "w") as file:
            file.write("\n".join(polygons))

        destination = osp.join(output_dir,"JPEGImages", f"{base}.jpg")
        cv2.imwrite(destination, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    print("Done!")

# transform_image_label("./result/JPEGImages","./result/Labels","./result/Transform")
    


