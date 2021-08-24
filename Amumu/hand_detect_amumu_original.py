import imutils
import numpy as np
import cv2
import os

amumus = 'amumus'
current_path = os.getcwd()
medias = os.path.join(current_path, amumus)
print(current_path)
motions = os.listdir(medias)
save_folder = 'saved_amumu'
save_folder_path = os.path.join(os.getcwd(), save_folder)

lower = np.array([0,125,77], dtype = "uint8")
upper = np.array([255, 200, 150], dtype = "uint8")

def biggestContour(contours):
    x = 0
    y = 0
    w = 0
    h = 0
    contour = []
    for temp_contour in contours:
        temp_x,temp_y,temp_w,temp_h = cv2.boundingRect(temp_contour)
        if w*h < temp_w * temp_h:
            x = temp_x
            y = temp_y
            w = temp_w
            h = temp_h

    return (x, y, w, h)

def makeMask(frame):
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    skinMask = cv2.inRange(converted, lower, upper)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,3))
    skinMask = cv2.erode(skinMask, kernel, iterations = 6)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,2))
    skinMask = cv2.dilate(skinMask, kernel, iterations = 1)
    
    skinMask = cv2.GaussianBlur(skinMask, (3,3), 0)

    return skinMask

def makeRec(frame):
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    skinMask = cv2.inRange(converted, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15))
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    
    skinMask = cv2.GaussianBlur(skinMask, (3,3), 0)

    contours,_ = cv2.findContours(skinMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return biggestContour(contours)

j = 0
for motion in motions:
    save_path = os.path.join(save_folder_path, motion)
    hands_path = os.path.join(medias, motion)
    hands = os.listdir(hands_path)
    #print(hands)
    
    for hand in hands:

        hand_path = os.path.join(hands_path, hand)

        camera = cv2.VideoCapture(hand_path)
        
        i = 0

        while True:
            original_hand_data_name = hand + f'_{i}' + '.jpg'
            masked_hand_data_name = hand + '_masked' + f'_{i}' + '.jpg'
            coordinate_hand_data_name = hand + '_coord' + f'_{i}' + '.txt'

            grabbed, frame = camera.read()
            if not grabbed: break

            img_height, img_width, _ = frame.shape            

            forMask = makeMask(frame)
            cv2.imwrite(os.path.join(save_path, original_hand_data_name),frame)
            cv2.imwrite(os.path.join(save_path, masked_hand_data_name),forMask)
            
            x,y,w,h = makeRec(frame)
            rel_center_x = (x + (w / 2))/img_width
            rel_center_y = (y + (h / 2))/img_height
            rel_w = w / img_width
            rel_h = h / img_height
            motion_label = j
            f = open(os.path.join(save_path, coordinate_hand_data_name), "w")
            f.write(f"{motion_label} {rel_center_x} {rel_center_y} {rel_w} {rel_h}\n")
            i += 1
        
    j += 1