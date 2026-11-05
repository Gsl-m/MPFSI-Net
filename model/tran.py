import numpy as np
import random
from PIL import Image

class ImageAugmentation:
    def __init__(self, images, masks):
        self.images = images
        self.masks = masks
        self.image_height, self.image_width = self.images.shape[2], self.images.shape[3]
        self.sub_region_height = self.image_height // 4
        self.sub_region_width = self.image_width // 4

    def apply_data_augmentation(self):
        batch_size = self.images.shape[0]
        augmented_images = []
        augmented_masks = []

        for i in range(batch_size):
            # 将原始图像分成4个子区域
            sub_images = self.split_image_into_subregions(self.images[i, 0])
            sub_masks = self.split_mask_into_subregions(self.masks[i, 0])

            # 对每个子区域应用数据增强
            for j in range(4):
                if random.random() < 0.5:  # 50%的概率应用数据增强
                    sub_image, sub_mask = self.apply_augmentation_to_subregion(sub_images[j], sub_masks[j])
                    sub_images[j] = sub_image
                    sub_masks[j] = sub_mask

            # 将增强后的子区域合并回原始图像和掩码
            augmented_image = self.merge_subregions_into_image(sub_images)
            augmented_mask = self.merge_subregions_into_mask(sub_masks)

            augmented_images.append(np.expand_dims(augmented_image, axis=0))
            augmented_masks.append(np.expand_dims(augmented_mask, axis=0))

        return np.concatenate(augmented_images, axis=0), np.concatenate(augmented_masks, axis=0)

    def split_image_into_subregions(self, image):
        sub_images = []
        for y in range(0, self.image_height, self.sub_region_height):
            for x in range(0, self.image_width, self.sub_region_width):
                sub_image = Image.fromarray((image[y:y+self.sub_region_height, x:x+self.sub_region_width] * 255).astype(np.uint8))
                sub_images.append(sub_image)
        return sub_images

    def split_mask_into_subregions(self, mask):
        sub_masks = []
        for y in range(0, self.image_height, self.sub_region_height):
            for x in range(0, self.image_width, self.sub_region_width):
                sub_mask = Image.fromarray((mask[y:y+self.sub_region_height, x:x+self.sub_region_width] * 255).astype(np.uint8))
                sub_masks.append(sub_mask)
        return sub_masks

    def apply_augmentation_to_subregion(self, sub_image, sub_mask):
        # 对子区域应用 90°、180°、270° 旋转以及水平和垂直翻转
        augmentation_mode = random.choices([0, 90, 180, 270, 'horizontal', 'vertical'], weights=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1], k=1)[0]
        if augmentation_mode == 0:
            return sub_image, sub_mask
        elif augmentation_mode == 90:
            return sub_image.rotate(90, resample=Image.BICUBIC), sub_mask.rotate(90, resample=Image.BICUBIC)
        elif augmentation_mode == 180:
            return sub_image.rotate(180, resample=Image.BICUBIC), sub_mask.rotate(180, resample=Image.BICUBIC)
        elif augmentation_mode == 270:
            return sub_image.rotate(270, resample=Image.BICUBIC), sub_mask.rotate(270, resample=Image.BICUBIC)
        elif augmentation_mode == 'horizontal':
            return sub_image.transpose(Image.FLIP_LEFT_RIGHT), sub_mask.transpose(Image.FLIP_LEFT_RIGHT)
        elif augmentation_mode == 'vertical':
            return sub_image.transpose(Image.FLIP_TOP_BOTTOM), sub_mask.transpose(Image.FLIP_TOP_BOTTOM)

    def merge_subregions_into_image(self, sub_images):
        merged_image = np.zeros((self.image_height, self.image_width), dtype=np.uint8)
        for i, sub_image in enumerate(sub_images):
            x = (i % 4) * self.sub_region_width
            y = (i // 4) * self.sub_region_height
            merged_image[y:y+self.sub_region_height, x:x+self.sub_region_width] = np.array(sub_image)
        return merged_image

    def merge_subregions_into_mask(self, sub_masks):
        merged_mask = np.zeros((self.image_height, self.image_width), dtype=np.uint8)
        for i, sub_mask in enumerate(sub_masks):
            x = (i % 4) * self.sub_region_width
            y = (i // 4) * self.sub_region_height
            merged_mask[y:y+self.sub_region_height, x:x+self.sub_region_width] = np.array(sub_mask)
        return merged_mask