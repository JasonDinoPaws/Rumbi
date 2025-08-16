# This is to get the camera feed from the pi camera and makes it into a bytes

import cv2
from picamera2 import Picamera2
import numpy as np


class Camera:
    def __init__(self,width=1640,hight=1232,fl=False,ftype=".jpg"):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_video_configuration({"size": (width, hight)}))
        self.camera.start()
        self.frame = None

        self.flip = fl
        self.file_type = ftype
        pass

    def flip_if_needed(self,frame): #will flip the camera if oriented wrong
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self): #this code is unused but it will get our current frame
        frame = self.camera.capture_array()
        frame = self.flip_if_needed(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        ret, jpg = cv2.imencode(self.file_type, frame)
        self.frame = jpg.tobytes()

    