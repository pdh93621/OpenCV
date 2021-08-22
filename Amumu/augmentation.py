import cv2
import random
import numpy as np
import os
import time

# 이미지 경로 = 변환 이미지 저장 경로
img_path = 'D:/Hyens_Projects/OpenCV/Amumu/motions'
# 좌표 경로 = 좌표 저장 경로
coordinate_path = 'D:/Hyens_Projects/OpenCV/Amumu/coordinate'
# 배수 설정: n배 -> n-1입력
multi_num = 2

# 좌우 반전
def LR_flip(image):
    return cv2.flip(image, 1)

# 좌우 반전 좌표 반환(원래 x값 -> 1-x, 나머지 좌표는 그대로)
def LR_flip_coord(coord):
    flip_coord = coord
    flip_coord[1] = str(1 - float(flip_coord[1]))
    return ' '.join(flip_coord)   

# 밝기 조절
def change_brightness(image, TF):
    if TF:
        alpha_range = range(2,19)
        return cv2.convertScaleAbs(image, alpha = 0.1 * random.choice(alpha_range)) 
    return image

# H,S 조절
def change_hsv(image, TF):
    if TF:
        image_hsv = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        h, s, v = cv2.split(image_hsv)
        new_h = ((h.astype('int32') + random.choice(range(5,70))) % 180).astype('uint8')
        new_s = s + random.choice(range(5,20))
        new_img = np.array([new_h, new_s, v]).transpose((1,2,0))
        return cv2.cvtColor(new_img, cv2.COLOR_HSV2BGR)
    return image

def popRice(multi_num, image, name):
    #밝기 조절 여부, 색상+채도 조절 여부
    trans = [[False,True], [True,False], [True,True]]
    for i in range(multi_num):
        bright_change, hsv_change = random.choice(trans)
        trans_image = change_brightness(image, bright_change)
        trans_image = change_hsv(trans_image, hsv_change)
        cv2.imwrite(os.path.join(img_path, name + f'_trans{i}' + '.jpg'), trans_image)
        coord = open(os.path.join(coordinate_path, name + '.txt'),"r").readline()
        #print(os.path.join(coordinate_path, name + '.txt'))
        trans_coord = open(os.path.join(coordinate_path, name + f'_trans{i}' + '.txt'), "w")
        trans_coord.write(coord)
        trans_coord.close()

names = [image.split('.')[0] for image in os.listdir(img_path)]

for name in names:
    image = cv2.imread(os.path.join(img_path, name + '.jpg'))
    cv2.imwrite(os.path.join(img_path, name + '_flip'+ '.jpg'), LR_flip(image))
    coord = open(os.path.join(coordinate_path, name + '.txt'),"r").readline().split()
    flip_coord = open(os.path.join(coordinate_path, name + '_flip' + '.txt'), "w")
    flip_coord.write(LR_flip_coord(coord))
    flip_coord.close()

names = [image.split('.')[0] for image in os.listdir(img_path)]
#print(names)
for name in names:
    image = cv2.imread(os.path.join(img_path, name + '.jpg'))
    popRice(multi_num, image, name)