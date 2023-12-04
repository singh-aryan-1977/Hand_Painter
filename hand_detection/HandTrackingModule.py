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
    def __init__(self,mode=False,max_hands=2,model_complexity=1,detection_conf=0.5, track_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity=model_complexity
        self.detection_conf = detection_conf
        self.track_conf = track_conf
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complexity, self.detection_conf, self.track_conf)
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4,8,12,16,20]
        
    
    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hands_on_screen in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hands_on_screen, self.mp_hands.HAND_CONNECTIONS)
        return img
    
    def find_position(self, img, hand_number=-1, draw=True):
        
        self.landmark_list = []
        if hand_number == -1:
            if self.results.multi_hand_landmarks:
                for hands_on_screen in self.results.multi_hand_landmarks:
                    for id, landmark in enumerate(hands_on_screen.landmark):
                        height, width, _ = img.shape
                        cx, cy = int(landmark.x * width), int(landmark.y*height)
                        self.landmark_list.append([id,cx,cy])
                        if draw:
                            cv2.circle(img, (cx, cy), 15, (172,192,85), cv2.FILLED)
        else:
            # print("got here")
            # print(handNumber)
            if self.results.multi_hand_landmarks:
                hands_on_screen = self.results.multi_hand_landmarks[hand_number]
                for id, landmark in enumerate(hands_on_screen.landmark):
                    height, width, channels = img.shape
                    cx, cy = int(landmark.x * width), int(landmark.y*height)
                    self.landmark_list.append([id,cx,cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 15, (172,192,85), cv2.FILLED)
        
        return self.landmark_list
    
    def find_fingers_up(self):
        fingers = []
        
        # For thumb
        if self.landmark_list[self.tip_ids[0]][1] < self.landmark_list[self.tip_ids[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        for id in range(1, 5):
            if self.landmark_list[self.tip_ids[id]][2] < self.landmark_list[self.tip_ids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


def main():
    p_time = 0
    c_time = 0
    camera = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = camera.read()
        if success:
            img = detector.find_hands(img)
            detector.find_position(img)
            c_time = time.time()
            fps = 1/(c_time-p_time)
            p_time = c_time
        
            # cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,3, (255,0,255), 3)
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