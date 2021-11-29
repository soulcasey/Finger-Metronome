import cv2
import mediapipe
import Final_Json
from sys import platform

camera = cv2.VideoCapture(0) #Turn on webcam
camera.set(3, 900) #Set webcam screen width
camera.set(4, 500) #Set webcam screen height

class handDetector():
    def __init__(self):
        if(platform == "win32" or platform == "darwin"): #If run on Windows or Mac
            self.hand = mediapipe.solutions.hands.Hands(False,1,1,0.2,0.2) #Set hand detection configuration
        else: #If run on Pi
            self.hand = mediapipe.solutions.hands.Hands(False,1,0.2,0.2)
 
    def findHands(self, image): #Detect hand
        self.detect = self.hand.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if(self.detect.multi_hand_landmarks):
            for handPlot in self.detect.multi_hand_landmarks:
                mediapipe.solutions.drawing_utils.draw_landmarks(image, handPlot, mediapipe.solutions.hands.HAND_CONNECTIONS) #Draw skeleton lines on hand
        return image
 
    def findFingerCount(self, image): #Detect up fingers
        self.fingerCount = 0 #Number of fingers up
        fingerIndex = [4, 8, 12, 16, 20] #Finger tip index numbers from mediapipe
        fingerPosition = [] #All finger indexes
        if(self.detect.multi_hand_landmarks):
            myHand = self.detect.multi_hand_landmarks[0]
            for id, landmarks in enumerate(myHand.landmark):
                height, width, c = image.shape
                x, y = int(landmarks.x * width), int(landmarks.y * height)
                fingerPosition.append([id, x, y]) #Adds finger position indexes to the list
        if(len(fingerPosition) != 0): #If hand is detected
            for finger in range(0,5):
                if(finger == 0): #Thumb
                    thumbTip = fingerPosition[fingerIndex[finger]][1] #Thumb tip position
                    thumbDip = fingerPosition[fingerIndex[finger]-1][1] #Thumb dip position
                    whichHand = "" #Check if hand is left or right
                    for id, classification in enumerate(self.detect.multi_handedness):
                         whichHand = classification.classification[0].label #Detect left or right hand
                    if(whichHand == "Right" and thumbTip < thumbDip): #If right thumb tip is inside of thumb dip by folding the thumb
                        self.fingerCount += 1
                    elif(whichHand == "Left" and thumbTip > thumbDip): #If left thumb tip is inside of thumb dip by folding the thumb
                        self.fingerCount += 1    
                else: #Index, middle, ring, pinky finger
                    fingerTip = fingerPosition[fingerIndex[finger]][2] #Finger tip position
                    fingerPip = fingerPosition[fingerIndex[finger]-2][2] #Finger pip position
                    if(fingerTip < fingerPip): #If finger tip is below finger pip by folding the finger
                        self.fingerCount += 1
        else: #If there is no hand detected
            self.fingerCount = "No Hand"
        return self.fingerCount

detector = handDetector()

def tempo(x): #Get tempo value
    Final_Json.save(x) #Save the new tempo value to Json
    print(x)

cv2.namedWindow('Hand Metronome') #Create windows
cv2.createTrackbar("Tempo", "Hand Metronome", Final_Json.load(), 200, tempo) #Create tempo slider with saved Json value

def cameraActivate():
    success, screen = camera.read() #Read the webcam
    screen = cv2.flip(screen,1) #Flip camera to mirror
    screen = detector.findHands(screen) #Overlay skeleton lines on camera screen
    cv2.putText(screen, str(detector.findFingerCount(screen)), (50,100), cv2.FONT_ITALIC, 2, (255,200,0),2) #Display text
    cv2.imshow("Hand Metronome",screen) #Display webcam screen
    cv2.waitKey(1) #Camera frame wait time