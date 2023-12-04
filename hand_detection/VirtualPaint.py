import HandTrackingModule as htm
import cv2
import os
import numpy as np

folder_path = "./paint_headers"
img_paths = os.listdir(folder_path)
img_paths.remove('.DS_Store')

HEADER_HEIGHT = 125
HEADER_WIDTH = 1280

#Global variables initializations
draw_color = (51,255,255)
brush_thickness = 15
eraser_thickness = 100
xp,yp = 0,0

show_drawing_canvas = True
        
# Getting all headers from files
overlay_list = {}
for path in img_paths:
    img = cv2.imread(f'{folder_path}/{path}')
    overlay_list[path]= img

# Getting headers and magnifying sidebars
header = overlay_list['normal.png']
magnifying_sidebar = overlay_list['magnifying.png']


# Setting window size
camera = cv2.VideoCapture(0)
camera.set(3, 1280) # Width
camera.set(4,720) # Height

# Setting drawing canvas
drawing_canvas = np.zeros((720, 1280, 3), np.uint8)

#importing hand detector module
detector = htm.handDetector(detection_conf=0.85)


# Function to handleMagnifying increases and decreases
def handleMagnifying(ring_x3, ring_y3):
    global brush_thickness
    global eraser_thickness
    if ring_x3 < 100:
        if 270 < ring_y3 < 320:
            if brush_thickness >= 200:
                return
            brush_thickness += 10
            # print("Reached magnifying increase for paintbrush")
        elif 360 < ring_y3 < 400:
            if brush_thickness <= 10:
                return
            brush_thickness -= 10
            # print("Reached magnifying decrease for paintbrush")
        elif 500 < ring_y3 < 540:
            if eraser_thickness >= 200:
                return
            eraser_thickness += 10
            # print("Reached magnifying increase for eraser")
        elif 580 < ring_y3 < 610:
            # print("reached magnifting decrease for eraser")
            if eraser_thickness <= 10:
                return
            eraser_thickness -= 10
    return 

while True:
    success, img = camera.read()
    if success:   
        img = cv2.flip(img, 1)
        
        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=False)
        
        
        selection_mode = False
        drawing_mode = False
        if len(lm_list) != 0:
            # print(lmList[8])
            x1,y1 = lm_list[8][1:] # Index finger tip
            x2,y2 = lm_list[12][1:] # Middle finger tip
            x3,y3 = lm_list[16][1:] # Ring finger tip
            
            fingers = detector.find_fingers_up()
            # print(fingers)
            
            if fingers[1] and fingers[2]:
                # print("selection mode")
                xp,yp=0,0
                cv2.rectangle(img,(x1,y1-25),(x2,y2+25),draw_color, cv2.FILLED)
                selection_mode = True
                #Checking if we are at the header
                # print(x1, y1)
                if y1 < HEADER_HEIGHT:
                    # print("Reached here")
                    if x1 < 100:
                        header = overlay_list['normal.png']
                        draw_color = (51,255,255)
                    elif 100 < x1 < 170:
                        header = overlay_list['yellow.png']
                        draw_color = (51,255,255)
                    elif 260 < x1 < 340:
                        header = overlay_list['purple.png']
                        draw_color = (2550,0,255)
                    elif 450 < x1 < 520:
                        header = overlay_list['green.png']
                        draw_color = (0,255,0)
                    elif 690 < x1 < 760:
                        header = overlay_list['blue.png']
                        draw_color = (255,0,0)
                    elif 850 < x1 < 940:
                        header = overlay_list['red.png']
                        draw_color = (0,0,255)
                    elif 1070 < x1 < 1120:
                        header = overlay_list['eraser.png']
                        draw_color = (0,0,0)
                    else:
                        header = overlay_list['normal.png']
                        draw_color = (51,255,255)
            else:
                # print("not selection mode")
                selectionMode = False
                
            if fingers[1] and not fingers[2]:
                # print("drawing mode")
                cv2.circle(img, (x1,y1),15,draw_color,cv2.FILLED)
                drawing_mode = True
                if not xp and not yp:
                    xp,yp = x1,y1
                    
                if draw_color == (0,0,0):
                    # print("reached here")
                    # print(eraser_thickness)
                    cv2.line(img, (xp,yp), (x1,y1), draw_color, eraser_thickness)
                    cv2.line(drawing_canvas, (xp,yp),(x1,y1),draw_color,eraser_thickness)
                else:
                    cv2.line(img, (xp,yp), (x1,y1), draw_color, brush_thickness)
                    cv2.line(drawing_canvas, (xp,yp),(x1,y1),draw_color,brush_thickness)
                xp,yp=x1,y1
            else:
                # print("not drawing mode")
                drawing_mode = False
                
            if fingers[1] and fingers[2] and fingers[3]:
                # print("Index\n")
                # print(x1,y1)
                # print("Middle\n")
                # print(x2,y2)
                # print("Ring\n")
                # print(x3,y3)
                handleMagnifying(x3, y3)
                
        # Optimizing overlay of drawing canvas and original image        
        img_gray = cv2.cvtColor(drawing_canvas, cv2.COLOR_BGR2GRAY)
        _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, img_inv)
        img = cv2.bitwise_or(img, drawing_canvas)
        
        
        header = cv2.resize(header, (HEADER_WIDTH, HEADER_HEIGHT))
        magnifying_sidebar = cv2.resize(magnifying_sidebar, (100, 720-120))
        # print(magnifying_sidebar.shape)
        img[0:HEADER_HEIGHT, 0:HEADER_WIDTH] = header
        img[120:,0:100] = magnifying_sidebar
        # img = cv2.addWeighted(img,0.5,drawingCanvas,0.5,0)
        text_to_display = f'Brush Thickness: {brush_thickness} | Eraser Thickness: {eraser_thickness}'
        cv2.putText(img, text_to_display, (800, 150), cv2.FONT_HERSHEY_DUPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)
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