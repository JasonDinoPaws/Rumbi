# This Gives no website function 
# Edit everything but the website and camera
from os import geteuid,listdir,path
from time import sleep,time
from flask import Flask, render_template, Response, request, send_from_directory,jsonify,send_file
from AudioDownload import DownloadAudio
from Enums import *
import cv2
from  threading import Thread
from datetime import datetime
import Sounds


isSudo = geteuid() == 0
rpath = "".join(x+"/" for x in __file__.split("/")[:-1])
IsPi = input("IsPi (T,F): ").lower() == "t"
LoadSounds = input("Load Sounds (T,F): ").lower() == "t"


# Loads anything in a Dir both main and sub
def LoadDir(start,subdir=False):
    files = {}
    for x in listdir(start):
        if subdir and path.isdir(f"{start}/{x}"):
            files[x] = LoadDir(f"{start}/{x}",subdir)
        else:
            files[x] = f"{start}/{x}"
            
    return files

# Finds a file in a table of files
def FindFile(tab,fpath):
    if fpath[0] == "/":
        fpath = fpath[1:]

    np =  fpath.split('/',1)
    ind = np[0] in tab

    if ind and isinstance(tab[np[0]], dict):
        return FindFile(tab[np[0]],np[1])
    elif ind:
        return tab[np[0]]
    else:
        return False

# If the thing runnning is a pi , Mainly here for testing perposes of the site
if IsPi:
    from MotorController import Controller
    M = Controller(17,27,22,23)  

    # Leds  
    if isSudo:
        from Leds import Matrix,Strip
        Ma = Matrix(rows=8,cols=8,rotation=180)
        sleep(.005)
        Ma2 = Matrix(rows=8,cols=8,rotation=180,flip=True)
        sleep(.005)
        S = Strip(count=28)
        S.PlayAnimation(Animations.Random("Loading"))
        Ma.ShowImage("Eyes/loading.png")
        Ma2.ShowImage("Eyes/loading.png")



if __name__ == "__main__":
    if LoadSounds: # Loads the sounds in the Sounds folder
        Sounds.LoadSounds()

    input("Start?") # Prompt telling people everything is ready

    # Led States to default
    if IsPi and isSudo:
        Ma2.ShowImage("Eyes/idle.png")
        Ma.ShowImage("Eyes/idle.png")
        S.StopAnimation()
        S.ColorAll()
    
    # Plays startup sounds
    if LoadSounds:
        Sounds.Playsound("Opening.wav")
        Sounds.random(rpath+"Sounds/OpeningSFX")

    
    pages = {
        "home": {"header": "", "options": ["Head Leds","Face Leds","Movement","Sounds"]},
        "Head Leds": {"header": "", "options": []},
        "Face Leds": {"header": "", "options": []},
        "Movement": {"header": "", "options": []},
        "Sounds": {"header": "", "options": []},
    }
    page = "home"
    while True:
        if not page in pages:
            page = "home"
        data = pages[data]
        print(data.header,"\n")
        for x in range(len(data.options)):
            print(f"{x}. {data.options[x]}")
        ans = input("Answer: ")
        if ans.isdigit() and int(ans) >= 0 and int(ans) < len(data.options):
            page = pages.keys()[int(ans)]