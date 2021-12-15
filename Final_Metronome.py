import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
buzzer = GPIO.PWM(21,1000)

class metronome():
    def __init__(self):
        self.currentTime = time.time()
        self.order = 1 #Track order of beeps
        self.on = False
    
    def sound(self, finger):
        if(self.order == 1): #On first beep 
            buzzer.ChangeFrequency(1000)
            buzzer.start(1)
        else: #Every other beep
            
            buzzer.ChangeFrequency(500)
            buzzer.start(1)
        self.order += 1
        if(self.order > finger): #Reset order when passed number of fingers
            self.order = 1
    
    def beep(self, bpm, finger): #Algorithm for metronome pattern
        if(finger == 5 and not self.on):
            buzzer.ChangeFrequency(1000)
            buzzer.start(1)
            self.on = True
        
        if(finger > 0 and finger < 5):
            waitTime = 60 / (bpm * finger) #Calculate the wait time in seconds depending on the bpm and number of fingers up
            timePassed = time.time() - self.currentTime
            
            if(timePassed > 0.02 and self.on):
                buzzer.stop()
                self.on = False
            
            if(timePassed > waitTime):
                self.sound(finger)
                self.on = True
                self.currentTime = time.time()
        if(finger == 0):
            buzzer.stop()
            self.on = False

sound = metronome()
