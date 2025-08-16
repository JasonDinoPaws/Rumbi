# Connects everything together and starts a web server

from os import geteuid,listdir,path
from time import sleep,time
from flask import Flask, render_template, Response, request, send_from_directory,jsonify,send_file
from AudioDownload import DownloadAudio
from Enums import *
import cv2
from  threading import Thread
from datetime import datetime
import Sounds

# Inisulization
app = Flask(__name__)
isSudo = geteuid() == 0
rpath = "".join(x+"/" for x in __file__.split("/")[:-1])
IsPi = input("IsPi (T,F): ").lower() == "t"
TakeShots  = input("Save Camera Shots (T,F): ").lower() == "t"
LoadSounds = input("Load Sounds (T,F): ").lower() == "t"

# Starts a log, will make it so that you dont have a terminal anymore
if input("Create Log (T,F)").lower() == "t":
    import sys
    Log = open(f"{rpath}/Logs/{time()}.txt","+w")
    sys.stdout = Log
    sys.stderr = Log

# Redirects for shortend website path
fileredirects = {
    "Sounds": "Sounds.html",
    "Movement": "Movement.html",
    "Eyes": "Eyes.html",
    "Lights": "Lights.html"
}

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
    from Camera import Camera
    from MotorController import Controller
    C = Camera(820,616,fl=False)
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


# All files for only 2 parts
Websitefiles = LoadDir(rpath+"templates",True)
Imagefiles = LoadDir(rpath+"Images",True)


#Set Up
@app.route('/')
def index():
    return render_template('index.html') 

# return any website files 
@app.route('/<filename>')
def website_files(filename):
    if filename in fileredirects:
        filename = fileredirects[filename]

    if filename in Websitefiles:
        if filename[-5:] == ".html":
            return render_template(filename) 
        elif filename[-4:] == ".txt":
            return Response(open(f"{rpath}templates/{filename}","r").read(), mimetype='text/plain')
        
        return send_file(f"{rpath}templates/{filename}", as_attachment=True)
    return None

# return any images
@app.route('/Images/<path:filename>')
def iamge_files(filename):
    file = FindFile(Imagefiles,filename)
    if file:
        return send_file(file, as_attachment=True)
    return jsonify("Failed")


# Any image/info that can by dynamically updated, i.e camera
def gen(inst):
    while True:
        sleep(.05)
        frame=None
        if inst == "camera":
            frame = C.frame

        if frame != None:
            yield b'--frame\r\n' b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n'


# Gets any info like the sound and movement queue | Lights states and camera output
@app.route("/get/<path:filename>")
def getinfo(filename:str):
    objtype,inst = filename.split("/",1)
    if objtype == "queue":
        if inst == "Sounds": 
            return  [x[0:2] for x in Sounds.AudioQueue]
        elif inst == "Motor" and IsPi:
            return M.Queue
        else:
            return {}
    elif objtype == "lights":
        file = None
        match inst:
            case "head":
                if isSudo and IsPi and "S" in globals():
                    file = FindFile(Imagefiles,str(S.animation).replace(".","/")+".gif")
                if not file:
                    file = FindFile(Imagefiles,"Animations/Off.gif")

            case "face":
                if isSudo and IsPi and "Ma" in globals():
                    file = FindFile(Imagefiles,str(Ma.animation))
                if not file:
                    file = FindFile(Imagefiles,"Eyes/idle.png")

        return send_file(file, as_attachment=True)
    elif objtype == "video":
        return Response(gen(inst), 
                                mimetype='multipart/x-mixed-replace; boundary=frame')
    return

# Change any data i.e Leds states
@app.route("/chng/<path:filename>")
def Change(filename:str):
    typ,inst = filename.split("/",1)
    match typ:
        case "head":
            if "S" in globals():
                S.StopAnimation()
                if inst == "Full":
                    S.ColorAll()
                elif inst in Animations.__members__:
                    S.PlayAnimation(Animations[inst])
        case "face":
            if "Ma" in globals():
                if FindFile(Imagefiles,f"Eyes/{inst}.png"):
                    Ma2.ShowImage(f"Eyes/{inst}.png")
                    Ma.ShowImage(f"Eyes/{inst}.png")

    return "No returned"

# Wheels given its action and its duration
@app.route("/move/<action>/<dur>")
def move(action:str,dur:float):
    action = action.split(",")
    dur = float(float(dur))
    if IsPi:
        if len(action) > 1:
            M.Action(int(action[0]),dur/2)
            M.Action(int(action[1]),.24)
            M.Action(int(action[0]),dur/2)
        elif int(action[0]) == -1:
            M.Reset()
        else:
            M.Action(int(action[0]),dur)
    return jsonify(result="sent action")


# Sound already loaded
@app.route("/sound/")
def getounds():
    return [x for x in Sounds.loaded.keys()]

# Put a sound in the queue
@app.route("/sound/play/<name>")
def playsound(name:str):
    name = name.replace("⠀","/").replace("‎","?")
    
    if name.startswith("text:"):
        print(name[5:])
        return jsonify("no")
    elif name.startswith("http"):
        name = DownloadAudio(name)

    Sounds.Playsound(name)
    return jsonify(result=f"Played")


# Any const updateing to prevent it happening by like 50 people on the website
def Updateobjs():
     nt = 0
     while IsPi:
        time = datetime.now()
        C.get_frame()
        if TakeShots and time.second %2 == 0 and time.second != nt:
            nt = time.second
            with open(f"{rpath}/map/{time}.jpg","+wb") as file:
                file.write(C.frame)
            cv2.imwrite(f"{rpath}/map/{time}.jpg",C.frame)



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
    
    # Starting
    Thread(target=Updateobjs).start()
    app.run(host='0.0.0.0', debug=False, port=isSudo and "80" or "5000", threaded=True)