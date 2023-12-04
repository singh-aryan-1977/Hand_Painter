import cv2
import mediapipe as mp
import time

    
"""
WRIST = 0
  THUMB_CMC = 1
  THUMB_MCP = 2
  THUMB_IP = 3
  THUMB_TIP = 4
  INDEX_FINGER_MCP = 5
  INDEX_FINGER_PIP = 6
  INDEX_FINGER_DIP = 7
  INDEX_FINGER_TIP = 8
  MIDDLE_FINGER_MCP = 9
  MIDDLE_FINGER_PIP = 10
  MIDDLE_FINGER_DIP = 11
  MIDDLE_FINGER_TIP = 12
  RING_FINGER_MCP = 13
  RING_FINGER_PIP = 14
  RING_FINGER_DIP = 15
  RING_FINGER_TIP = 16
  PINKY_MCP = 17
  PINKY_PIP = 18
  PINKY_DIP = 19
  PINKY_TIP = 20
"""

class handDetector():
    def __init__(self,mode=False,maxHands=2,modelComplexity=1,detectionConf=0.5, trackConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity=modelComplexity
        self.detectionConf = detectionConf
        self.trackConf = trackConf
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20]
        
    
    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handsOnScreen in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handsOnScreen, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def find_position(self, img, handNumber=-1, draw=True):
        
        self.landmarkList = []
        if handNumber == -1:
            if self.results.multi_hand_landmarks:
                for handsOnScreen in self.results.multi_hand_landmarks:
                    for id, landmark in enumerate(handsOnScreen.landmark):
                        height, width, channels = img.shape
                        cx, cy = int(landmark.x * width), int(landmark.y*height)
                        self.landmarkList.append([id,cx,cy])
                        if draw:
                            cv2.circle(img, (cx, cy), 15, (172,192,85), cv2.FILLED)
        else:
            # print("got here")
            # print(handNumber)
            if self.results.multi_hand_landmarks:
                handsOnScreen = self.results.multi_hand_landmarks[handNumber]
                for id, landmark in enumerate(handsOnScreen.landmark):
                    height, width, channels = img.shape
                    cx, cy = int(landmark.x * width), int(landmark.y*height)
                    self.landmarkList.append([id,cx,cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 15, (172,192,85), cv2.FILLED)
        
        return self.landmarkList
    
    def find_fingers_up(self):
        fingers = []
        
        # For thumb
        if self.landmarkList[self.tipIds[0]][1] < self.landmarkList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        for id in range(1, 5):
            if self.landmarkList[self.tipIds[id]][2] < self.landmarkList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


def main():
    pTime = 0
    cTime = 0
    camera = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = camera.read()
        if success:
            img = detector.find_hands(img)
            detector.find_position(img)
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
        
            cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,3, (255,0,255), 3)
            cv2.imshow("Image", img)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            break
    
    
    camera.release()
    cv2.destroyAllWindows() 
    
    
    
if __name__ == "__main__":
    main()