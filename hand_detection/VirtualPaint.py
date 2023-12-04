import HandTrackingModule as htm
import cv2
import os

folderPath = "./paint_headers"
img_paths = os.listdir(folderPath)
img_paths.remove('.DS_Store')

indx_of_normal = -1
for i in range(0, len(img_paths)):
    if img_paths[i] == 'normal.png':
        indx_of_normal = i
        break
    
overlayList = []
for path in img_paths:
    img = cv2.imread(f'{folderPath}/{path}')
    overlayList.append(img)

header = overlayList[indx_of_normal]

camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(4,720)

detector = htm.handDetector(detectionConf=0.85)

while True:
    success, img = camera.read()
    if success:   
        img = cv2.flip(img, 1)
        
        img = detector.find_hands(img)
        lmList = detector.find_position(img, draw=False)
        
        
        selectionMode = False
        drawingMode = False
        if len(lmList) != 0:
            x1,y1 = lmList[8][1:] # Index finger tip
            x2,y2 = lmList[12][1:] # Middle finger tip
            
            fingers = detector.find_fingers_up()
            print(fingers)
            
            if fingers[1] and fingers[2]:
                print("selection mode")
                selectionMode = True
            else:
                print("not selection mode")
                selectionMode = False
                
            if fingers[1] and not fingers[2]:
                print("drawing mode")
                drawingMode = True
            else:
                print("not drawing mode")
                drawingMode = False
        
        header = cv2.resize(header, (1280, 125))
        img[0:125, 0:1280] = header
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        print("Error in showing image")
        break
    
camera.release()
cv2.destroyAllWindows() 