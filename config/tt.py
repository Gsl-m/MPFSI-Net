import cv2

label_path = '../../data/MSCOCO2014/annotations/train2014/COCO_train2014_000000326639.png'
label = cv2.imread(label_path, cv2.IMREAD_GRAYSCALE)
print(label)
