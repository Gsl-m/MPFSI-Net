import numpy as np

class RandomErasing(object):
    def __init__(self, region_w, region_h):
        self.region_w = region_w
        self.region_h = region_h

    def __call__(self, img, mask):
        if self.region_w < img.shape[1] and self.region_h < img.shape[0]:
            x1 = np.random.randint(0, img.shape[1] - self.region_w)
            y1 = np.random.randint(0, img.shape[0] - self.region_h)

            # 将图像的擦除区域设置为随机像素值
            img[y1:y1 + self.region_h, x1:x1 + self.region_w, 0] = np.random.randint(0, 256, size=(self.region_h, self.region_w))
            img[y1:y1 + self.region_h, x1:x1 + self.region_w, 1] = np.random.randint(0, 256, size=(self.region_h, self.region_w))
            img[y1:y1 + self.region_h, x1:x1 + self.region_w, 2] = np.random.randint(0, 256, size=(self.region_h, self.region_w))

            # 将掩码的擦除区域设置为 0
            mask[y1:y1 + self.region_h, x1:x1 + self.region_w] = 0

        return img, mask