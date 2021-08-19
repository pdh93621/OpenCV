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
    index = 0
    x = 0
    y = 0
    w = 0
    h = 0
    contour = []
    temp_index = 0
    for temp_contour in contours:
        temp_x,temp_y,temp_w,temp_h = cv2.boundingRect(temp_contour)
        if w*h < temp_w * temp_h:
            x = temp_x
            y = temp_y
            w = temp_w
            h = temp_h
            index = temp_index
        temp_index += 1
    

    return (x, y, w, h, index)

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


for motion in motions:
    save_path = os.path.join(save_folder_path, motion)
    hands_path = os.path.join(medias, motion)
    hands = os.listdir(hands_path)
    #print(hands)
    
    for hand in hands:

        hand_path = os.path.join(hands_path, hand)

        camera = cv2.VideoCapture(hand_path)

        while True:

            grabbed, frame = camera.read()
            if not grabbed: break       

            forMask = makeMask(frame)
            
            line,_ = cv2.findContours(forMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            _, _, _, _, index = biggestContour(line)
            
            cv2.drawContours(frame, line, -1, (0,0,0))

            #x,y,w,h = makeRec(frame)
            
            #cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,0), 3)
            cv2.imshow("images", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"): break
        
        cv2.destroyAllWindows()