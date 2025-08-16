# Really bad motor controller movement
# This doesn't support custom speeds

import RPi.GPIO as GPIO
from time import sleep
from threading import Thread

class Controller:
    # Inisualization of the pins and actions
    def __init__(self, p1:int,p2:int,p3:int,p4:int,actions:list[int]=[[1,0,1,0], [0,1,1,0], [0,1,0,1], [1,0,0,1]]):
        self.pins = [p1,p2,p3,p4]
        self.actions = actions
        self.motion = 0
        self.Queue = []
        GPIO.setmode(GPIO.BCM)
        for x in self.pins:
            GPIO.setup(x, GPIO.OUT)
        self.Reset()
        pass
    
    # Everything off
    def Reset(self):
        self.motion = 0
        self.Queue = []
        for x in self.pins:
            GPIO.output(x, False)

    # Runs its eueue
    def RunQueue(self):
        self.motion = 1
        while len(self.Queue) > 0:
            a,d = self.Queue.pop(0)
            print(a,d)

            for n in range(len(self.actions[a])):
                GPIO.output(self.pins[n], self.actions[a][n])
            sleep(d)
        self.Reset()

    # Given the id and its duration adds it to the queue
    def Action(self,action:int,dur:float):
        if action >= 0 and action < len(self.actions) and dur > 0 and dur < 10:
            self.Queue.append((action,dur))

            if self.motion == 0:
                Thread(target=self.RunQueue,daemon=True).start()
