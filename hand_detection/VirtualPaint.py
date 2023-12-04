import HandTrackingModule as htm
import cv2
import os

folderPath = "./paint_headers"
img_paths = os.listdir(folderPath)
img_paths.remove('.DS_Store')

HEADER_HEIGHT = 125
HEADER_WIDTH = 1280

indx_of_normal = -1
for i in range(0, len(img_paths)):
    if img_paths[i] == 'normal.png':
        indx_of_normal = i
        break
    
overlayList = {}
for path in img_paths:
    img = cv2.imread(f'{folderPath}/{path}')
    overlayList[path]= img

header = overlayList['normal.png']

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
            # print(lmList[8])
            x1,y1 = lmList[8][1:] # Index finger tip
            x2,y2 = lmList[12][1:] # Middle finger tip
            
            fingers = detector.find_fingers_up()
            # print(fingers)
            
            if fingers[1] and fingers[2]:
                # print("selection mode")
                cv2.rectangle(img,(x1,y1-25),(x2,y2+25),(255,0,255), cv2.FILLED)
                selectionMode = True
                #Checking if we are at the header
                print(x1, y1)
                if y1 < HEADER_HEIGHT:
                    print("Reached here")
                    if x1 < 100:
                        header = overlayList['normal.png']
                    elif 100 < x1 < 170:
                        header = overlayList['yellow.png']
                    elif 260 < x1 < 340:
                        header = overlayList['purple.png']
                    elif 450 < x1 < 520:
                        header = overlayList['green.png']
                    elif 690 < x1 < 760:
                        header = overlayList['blue.png']
                    elif 850 < x1 < 940:
                        header = overlayList['red.png']
                    elif 1070 < x1 < 1120:
                        header = overlayList['eraser.png']
                    else:
                        header = overlayList['normal.png']
            else:
                # print("not selection mode")
                selectionMode = False
                
            if fingers[1] and not fingers[2]:
                # print("drawing mode")
                cv2.circle(img, (x1,y1),15,(255,0,255),cv2.FILLED)
                drawingMode = True
            else:
                # print("not drawing mode")
                drawingMode = False
        
        header = cv2.resize(header, (HEADER_WIDTH, HEADER_HEIGHT))
        img[0:HEADER_HEIGHT, 0:HEADER_WIDTH] = header
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        print("Error in showing image")
        break
    
camera.release()
cv2.destroyAllWindows() 