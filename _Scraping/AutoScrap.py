import requests
from bs4 import BeautifulSoup
import time
from random import *
import os.path
import youtube_dl

url = 'https://www.youtube.com/'
response = requests.get(url)

timeout = 3600  
timeout_start = time.time()

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

while time.time() < timeout_start + timeout:
    if response.ok:
        soup = BeautifulSoup(response.text)
        URL = soup.find('a')
    URL = str(URL)
    liste = [str(URL)]
    N = choice(liste)

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': SITE_ROOT + '/Audios/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([N])

    time.sleep(3)

    