# This is mainly just to download youtube videos audio given their link and saves it to a folder in tmp called Audios

import yt_dlp
from os import path,makedirs,listdir,remove,rename
import re
from random import randint

output_folder="/tmp/Audios"
downQueue = []

# If folder doesn't exists creates it
if not path.exists(output_folder):
    makedirs(output_folder)
else:
    for x in listdir(output_folder):
        remove(f"{output_folder}/{x}")

# the format to save the videos
ydl_opts = {
    'format': 'bestaudio/best',  # Download the best audio quality
    'extractaudio': True,  # Extract audio
    'outtmpl': path.join(output_folder, '%(title)s.%(ext)s'),  # Save file in the specified output folder
}

# Downloads only 1 video and returns its path
def Youtube(url:str):
    if re.search(r"https://(www|music).youtube.com/watch?",url):
        arlist = re.search(r"&list=",url)

        if arlist:
            url = url[:arlist.start()]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            file_extension = info_dict.get('ext', 'mp3')
            ydl.download([url])
        
        return f"{output_folder}/{video_title}.{file_extension}"
    return None


# Check if the video is a youtube video and sends it to download and puts it in a queue if there is more than 1
def DownloadAudio(url:str):
    retu = None
    name = f"{len(downQueue)}|{url}"
    downQueue.append(name)
    while downQueue.index(name) > 0:
        pass 

    if url.lower().startswith("https://youtu.be/"):
        url = "https://www.youtube.com/watch?v="+url[17:]
    try:
        if re.search(r"youtube",url):
            retu = Youtube(url)
    except:
        pass
    
    downQueue.pop(0)
    return retu