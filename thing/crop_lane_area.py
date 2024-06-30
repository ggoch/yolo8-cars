import cv2

# 读取图像
image_path = "./0babf32a-d6ff-3eaf-4cab-3a0a72ec1d89_front00000009.jpg"

def crop_lane_area(image):
    """
    裁切車道圖片中間區域。

    讓左右兩邊的車道線不會影響模型的預測結果。
    """

    # 取得影像尺寸
    height, width, _ = image.shape

    # 定义中间区域的宽度比例，例如保留中间 50% 的区域
    crop_width_ratio = 0.6

    # 計算中間區域的起始和結束位置
    start_x = int((width * (1 - crop_width_ratio)) / 2)
    end_x = int(start_x + (width * crop_width_ratio))

    # 裁剪中間區域
    cropped_image = image[:, start_x:end_x]

    # 顯示原始影像和裁剪後的影像
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Cropped Image', cropped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return cropped_image

    # 保存裁剪后的图像
    # cropped_image_path = "/mnt/data/cropped_image.jpg"
    # cv2.imwrite(cropped_image_path, cropped_image)

    # print(f"Cropped image saved to {cropped_image_path}")

# image = cv2.imread(image_path)
# crop_lane_area(image)