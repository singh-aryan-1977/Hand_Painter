import cv2
import mediapipe as mp
import time

camera = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = CTime = 0
while True:
    success, img = camera.read()
    if success:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        
        if results.multi_hand_landmarks:
            for handsOnScreen in results.multi_hand_landmarks:
                for id, landmark in enumerate(handsOnScreen.landmark):
                    height, width, channels = img.shape
                    cx, cy = int(landmark.x * width), int(landmark.y*height)
                    if id == 14: # Can change latr
                        cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                mpDraw.draw_landmarks(img, handsOnScreen, mpHands.HAND_CONNECTIONS)
        
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,3, (255,0,255), 3)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        print("Error in showing video capture")
        break
    
camera.release()
cv2.destroyAllWindows()