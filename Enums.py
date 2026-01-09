from enum import Enum
from random import randint

class Animations(Enum):
    Loading1 = {"Anim":[[1,0,-1]], "speed":.075}
    Loading2 = {"Anim":[[-1,0,1, 13,14,15]], "speed":.075}
    Loading3 = {"Anim":[[-1,0,1 ,6,7,8, 13,14,15, 20,21,22,]], "speed":.075}
    Loading4 = {"Anim":[[-2,-1,0]],"skip": 9, "speed":.2}
    Loading5 = {"Anim":[[0,1,2,3,4,5,6,7,8,9,10,11,12,13]],"speed":.075,"overflow":False,"startoff":13}
    Loading6 = {"Anim":[[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]], "speed":.075}

    def Random(Starts:str=""):
        Anims = []
        for x in Animations.__members__:
            if x.lower().startswith(Starts.lower()):
                Anims.append(x)
        
        return Animations[Anims[randint(0,len(Anims)-1)]]