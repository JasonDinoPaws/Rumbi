from pydub import AudioSegment
from pydub.playback import play
from os import listdir,walk,remove
from threading import Thread
from random import randint
from time import sleep

loaded = {}
loadeddir=[]
AudioQueue = []
Playing = False
path = "".join(x+"/" for x in __file__.split("/")[:-1])+"Sounds"
skip = False

def Queue():
    global AudioQueue,Playing
    Playing = True
    while len(AudioQueue) > 0:
        play(AudioQueue.pop(0)[2])
    Playing = False

def Loadsounds(folder:str,path:str=path):
    for _,dirc,_ in walk(path):
        if folder in dirc:
            break
    else:
        return
    
    for name in listdir(f"{path}/{folder}"):
        loaded[name] = AudioSegment.from_file(f"{path}/{folder}/{name}")
    loadeddir.append(folder)


def GetSound(name:str,path=path):
    if type(name) != type("f"):
        return False
    
    for k in loaded.keys():
        if k == name:
            return loaded[k]
    try:
        if name.startswith("/"):
            return AudioSegment.from_file(name)
        else:
            for root,_,files in walk(path):
                if name in files:
                    loaded[name] = AudioSegment.from_file(f"{root}/{name}")
                    print("loaded sound")
                    return loaded[name] 
    except Exception as e:
        print(e)
        pass
    
    return False

def Playsound(name:str,path=path):
    global AudioQueue
    sound = GetSound(name,path)
    if sound:
        if name.startswith("/tmp/"):
            remove(name)

        AudioQueue.append([name,sound.duration_seconds,sound])

        if not Playing:
            Thread(target=Queue,daemon=True).start()

def random(fpath=path):
    if fpath != path:
        keys = listdir(fpath)
    else:
        keys = [x for x in loaded.keys()]
    
    Playsound(keys[randint(0,len(keys)-1)],path=fpath)

def PlayAll(fpath=path,delay=0):
    if fpath != path:
        keys = listdir(fpath)
    else:
        keys = [x for x in loaded.keys()]

    for x in keys:
        Playsound(x,path=fpath)
        sleep(delay)

def LoadSounds():
    for _,dirc,_ in walk(path):
        for x in dirc:
            Loadsounds(x)
            Playsound(x)