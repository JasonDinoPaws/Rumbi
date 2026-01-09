from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO
from time import sleep
from cv2 import imread
import numpy as np
from threading import Thread
from Enums import Animations


rgb = [80,20,50]
path = "".join(x+"/" for x in __file__.split("/")[:-1])+"Images"
GPIO.setwarnings(False)

pixcount = 0
pin = 18
freq = 800000
dms = 10
invert = False
brightness = 15
MainStrip = PixelStrip(pixcount,pin,freq, dms, invert, brightness)
MainStrip.begin()

def IsValidColor(color,value):
    if type(value) == type("str") and value.isdigit():
        value = int(value)
    elif type(value) != type(0):
        value = rgb[color]

    return value

def CheckValue(AnimData,id,default,types=None):
    has = id in AnimData
    if types == None:
        types = (type(default))
    elif not type(types) is tuple:
        types = (types)
        

    if has and isinstance(AnimData[id],types):
        return AnimData[id]

    return default

def play(slef,Anim:Animations,Repeat,R,G,B):
    global MainStrip
    AnimData = Anim.value
    speed =  CheckValue(AnimData,"speed",.05,(int,float))
    skip = CheckValue(AnimData,"skip",1)
    overflow = CheckValue(AnimData,"overflow",True)
    startoff = CheckValue(AnimData,"startoff",0)

    ledamount = int((slef.count+startoff)/skip)

    AnimA = []
    for i in range(ledamount):
        AnimA.append([])
        for pixs in AnimData["Anim"]:
            for x in pixs:
                AnimA[len(AnimA)-1].append(((i-startoff)*skip)+x)

        
    i = 0
    print(f"playing animation {Anim}")
    while slef.animation == Anim:
        for x in AnimA[i-1]:
            slef.ColorPixel(x,[0,0,0],overflow)

        for x in AnimA[i]:
            slef.ColorPixel(x,[R,G,B],overflow)

        MainStrip.show()
        i += 1
        if i >= ledamount:
            if Repeat:
                i = 0
            else:
                break

        sleep(speed)

def ColorPixel(num, Colors=rgb, Show=False):
    num = int(num)
    R = IsValidColor(0,Colors[0])
    G = IsValidColor(1,Colors[1])
    B = IsValidColor(2,Colors[2])

    if num > -1 and num < pixcount:
        MainStrip.setPixelColor(num, Color(R,G,B))
        if Show:
            MainStrip.show()

class Matrix:
    def __init__(self, rows=8, cols=32, pin=18, invert = False, rotation=0, flip=False):
        global MainStrip,pixcount
        self.start = pixcount
        print(f"New Pixel Matrix at {pixcount}")
        pixcount += (rows*cols)
        GPIO.setwarnings(False)
        MainStrip = PixelStrip(pixcount,pin,freq, dms, invert, brightness)
        MainStrip.begin()

        self.count = rows*cols
        self.Color = (80,20,50)
        self.array = np.zeros((rows,cols))
        self.animation = ""
        c = cols-1
        r = rows-1
        up = True

        for i in range(self.count):
            self.ColorPixel(i,Show=True)
            self.array[r][c] = i

            if (up and r != 0) or (not up and r != rows-1):
                if up:
                    r -= 1
                else:
                    r += 1
            else:
                up = not up
                c -= 1
            
            sleep(.005)

        self.Clear()
        if flip:
            self.array = np.fliplr(self.array )
        if rotation != 0:
            self.array = np.rot90(self.array, k=int(rotation/90)) 
            for r in self.array:
                for c in r:
                    self.ColorPixel(c,Show=True)
            sleep(.005)
            self.Clear()
    
    def ColorPixel(self, num, Colors=rgb, Show=False):
        num = int(num)
        if num > -1 and num < self.count:
            ColorPixel(self.start+num,Colors,Show)

    def Clear(self):
        global MainStrip
        for x in range(self.count):
            self.ColorPixel(x,[0,0,0])
        MainStrip.show()


    def ShowText(self,text:str,R=None,G=None,B=None):
        pass


    def ShowImage(self,image_name, fpath:str=path, R=None,G=None,B=None):
        global MainStrip
        print(f"{fpath}/{image_name}")
        if type(image_name) == type("string"):
            img = imread(f"{fpath}/{image_name}")
            self.animation = image_name
        elif type(image_name) == type(np.array(())):
            img = image_name
            self.animation = ""
        else:
            return
        
        if img.flatten().shape[0] <= self.count:
            return
        
        
        for r in range(len(img)):
            for c in range(len(img[r])):
                if img[r,c,0] > 0:
                    self.ColorPixel(self.array[r][c],[R,G,B])
                else:
                    self.ColorPixel(self.array[r][c],[0,0,0])

        MainStrip.show()


    def StopAnimation(self):
        self.animation = ""
        self.Clear()

    def PlayAnimation(self,Animation:Animations,Repeat=True,R=80,G=20,B=50):
        if self.animation != "":
            self.StopAnimation()

        self.animation = Animation
        Thread(target=play,args=(self,Animation,Repeat,R,G,B),daemon=True).start()
        
class Strip():

    def __init__(self, count=10,pin=18, invert = False):
        global MainStrip,pixcount
        print(f"New Pixel Strip at {pixcount}")
        self.start = pixcount
        pixcount += count
        GPIO.setwarnings(False)
        MainStrip = PixelStrip(pixcount,pin,freq, dms, invert, brightness)
        MainStrip.begin()

        self.count = count
        self.animation = ""
        self.Color = (80,20,50)

        for i in range(self.count):
            self.ColorPixel(i,Show=True)   
            sleep(.005)
        self.Clear()
        sleep(.1)
        pass

    def ColorPixel(self, num, Colors=rgb,overflow=True, Show=False):
        num = int(num)
        if overflow:
            if num < 0:
                num = self.count+num
            elif num >= self.count:
                num = num-self.count

        if num > -1 and num < self.count:
            ColorPixel(self.start+num,Colors,Show)

    def Clear(self):
        global MainStrip
        for x in range(self.count):
            self.ColorPixel(x,[0,0,0])
        MainStrip.show()

    def ColorAll(self,R=80,G=20,B=50):
        for x in range(self.count):
            self.ColorPixel(x,[R,G,B])
        MainStrip.show()
        self.animation = "Animations.Full"
    
    def StopAnimation(self):
        self.animation =  "Animations.Off"
        self.Clear()

    def PlayAnimation(self,Animation:Animations,Repeat=True,R=80,G=20,B=50):
        if self.animation != "":
            self.StopAnimation()

        self.animation = Animation
        Thread(target=play,args=(self,Animation,Repeat,R,G,B),daemon=True).start()