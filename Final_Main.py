import Final_Finger
import Final_Metronome
#import Final_Tkinter
#import Final_Pi

while(True):
    Final_Finger.cameraActivate() #Open camera
    tempo = Final_Finger.cv2.getTrackbarPos("Tempo", "Hand Metronome")
    finger = Final_Finger.detector.fingerCount
    if(finger == "No Hand"):
        finger = 0
    Final_Metronome.sound.beep(tempo, finger)