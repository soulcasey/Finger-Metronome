import time 

class metronome():
    def __init__(self):
        self.currentTime = time.time()
        self.order = 1 #Track order of beeps
    
    def sound(self, finger):
        if(self.order == 1): #On first beep
            print("High")
        else: #Every other beep
            print("Low")
        self.order += 1
        if(self.order > finger): #Reset order when passed number of fingers
            self.order = 1
    
    def beep(self, bpm, finger): #Algorithm for metronome pattern
        if(finger > 0):
            waitTime = 60 / (bpm * finger) #Calculate the wait time in seconds depending on the bpm and number of fingers up
            timePassed = time.time() - self.currentTime
            if(timePassed > waitTime):
                self.sound(finger)
                self.currentTime = time.time()

sound = metronome()
