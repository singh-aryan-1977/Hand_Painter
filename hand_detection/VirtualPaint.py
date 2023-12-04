import HandTrackingModule as htm
import cv2
import os
import numpy as np

folderPath = "./paint_headers"
img_paths = os.listdir(folderPath)
img_paths.remove('.DS_Store')

HEADER_HEIGHT = 125
HEADER_WIDTH = 1280

drawColor = (51,255,255)
brushThickness = 15
eraserThickness = 100
xp,yp = 0,0

showDrawingCanvas = True

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

drawingCanvas = np.zeros((720, 1280, 3), np.uint8)

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
                xp,yp=0,0
                cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor, cv2.FILLED)
                selectionMode = True
                #Checking if we are at the header
                print(x1, y1)
                if y1 < HEADER_HEIGHT:
                    print("Reached here")
                    if x1 < 100:
                        header = overlayList['normal.png']
                        drawColor = (51,255,255)
                    elif 100 < x1 < 170:
                        header = overlayList['yellow.png']
                        drawColor = (51,255,255)
                    elif 260 < x1 < 340:
                        header = overlayList['purple.png']
                        drawColor = (2550,0,255)
                    elif 450 < x1 < 520:
                        header = overlayList['green.png']
                        drawColor = (0,255,0)
                    elif 690 < x1 < 760:
                        header = overlayList['blue.png']
                        drawColor = (255,0,0)
                    elif 850 < x1 < 940:
                        header = overlayList['red.png']
                        drawColor = (0,0,255)
                    elif 1070 < x1 < 1120:
                        header = overlayList['eraser.png']
                        drawColor = (0,0,0,0)
                    else:
                        header = overlayList['normal.png']
                        drawColor = (51,255,255)
            else:
                # print("not selection mode")
                selectionMode = False
                
            if fingers[1] and not fingers[2]:
                # print("drawing mode")
                cv2.circle(img, (x1,y1),15,drawColor,cv2.FILLED)
                drawingMode = True
                if not xp and not yp:
                    xp,yp = x1,y1
                    
                if drawColor == (0,0,0):
                    cv2.line(img, (xp,yp), (x1,y1), drawColor, eraserThickness)
                    cv2.line(drawingCanvas, (xp,yp),(x1,y1),drawColor,eraserThickness)
                else:
                    cv2.line(img, (xp,yp), (x1,y1), drawColor, brushThickness)
                    cv2.line(drawingCanvas, (xp,yp),(x1,y1),drawColor,brushThickness)
                xp,yp=x1,y1
            else:
                # print("not drawing mode")
                drawingMode = False
        # Optimizing overlay of drawing canvas and original image        
        imgGray = cv2.cvtColor(drawingCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, drawingCanvas)
        
        header = cv2.resize(header, (HEADER_WIDTH, HEADER_HEIGHT))
        img[0:HEADER_HEIGHT, 0:HEADER_WIDTH] = header
        # img = cv2.addWeighted(img,0.5,drawingCanvas,0.5,0)
        cv2.imshow("Image", img)
        # cv2.imshow("Drawing canvas", drawingCanvas)
        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        print("Error in showing image")
        break
    
camera.release()
cv2.destroyAllWindows() 