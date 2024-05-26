import albumentations as A
import cv2
import random


class Transforms:
    def __init__(self, height=512, width=512):
        self.height = height
        self.width = width

    def UpdateHeightWidth(self, height, width):
        self.height = height
        self.width = width

    def D4(self, image, masks):
        D4_transforms = A.Compose(
            [
                # A.Resize(self.height//2, self.width//2, interpolation=cv2.INTER_LINEAR, p=1),
                # D4 Group augmentations
                A.HorizontalFlip(p=1),
                A.VerticalFlip(p=0.5),
                A.RandomRotate90(p=0.5),
                A.Transpose(p=0.5),
                # A.Normalize()
            ]
        )

        result = D4_transforms(image=image, masks=masks)

        image = result["image"]
        masks = result["masks"]

        return image, masks

    def geom(self, image, masks):
        MAX_SIZE = min(self.height, self.width)

        geom_transforms = A.Compose(
            [
                # A.Resize(self.height//2, self.width//2, interpolation=cv2.INTER_LINEAR, p=1),
                # D4 Group augmentations
                A.HorizontalFlip(p=0.5),
                A.VerticalFlip(p=0.5),
                A.RandomRotate90(p=0.5),
                A.Transpose(p=0.5),
                # crop and resize
                A.RandomSizedCrop(
                    min_max_height=(MAX_SIZE - 100, MAX_SIZE),
                    height=self.height,
                    width=self.width,
                    interpolation=cv2.INTER_LINEAR,
                    always_apply=False,
                    p=0.5,
                ),
                A.Resize(self.height, self.width, interpolation=cv2.INTER_LINEAR, p=1),
                # A.Normalize()
            ],
        )

        print(self.height, self.width)
        print(image.shape)
        print(masks.shape)

        result = geom_transforms(image=image, masks=masks)

        image = result["image"]
        masks = result["masks"]

        return image, masks

    def heavy(self, image, masks):
        heavy_transforms = A.Compose(
            [
                A.RandomRotate90(),
                A.Flip(),
                A.Transpose(),
                A.GaussNoise(),
                A.ShiftScaleRotate(
                    shift_limit=0.0625, scale_limit=0.1, rotate_limit=45, p=0.7
                ),
                A.OneOf(
                    [
                        A.MotionBlur(p=0.2),
                        A.MedianBlur(blur_limit=3, p=0.1),
                        A.Blur(blur_limit=3, p=0.1),
                    ],
                    p=0.5,
                ),
                A.OneOf(
                    [
                        A.Sharpen(alpha=(0.2, 0.5), lightness=(0.5, 1.0), always_apply=False, p=0.3),
                        A.Emboss(alpha=(0.2, 0.5), strength=(0.2, 0.7), always_apply=False, p=0.3),
                        A.RandomBrightnessContrast(),
                    ],
                    p=0.5,
                ),
                A.HueSaturationValue(p=0.3),
                # A.Normalize()
            ]
        )

        result = heavy_transforms(image=image, masks=masks)

        image = result["image"]
        masks = result["masks"]

        return image, masks
    
    def random(self, image, masks):
        return random.choice([self.D4,self.geom,self.heavy])(image,masks)
