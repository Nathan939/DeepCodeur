import requests
from bs4 import BeautifulSoup
import time
from random import *
import os.path
import youtube_dl

url = 'https://www.youtube.com/'
response = requests.get(url)

timeout = 60
timeout_start = time.time()
NUMBER_OF_FILES = 50

URLs = []

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# while time.time() < timeout_start + timeout:
if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.findAll('a')
    for link in links:
        if len(link.get('href')) > 2 and link.get('href')[1] == 'w' and link.get('href') not in URLs:
            URLs.append(link.get('href'))
        if len(URLs) >= NUMBER_OF_FILES:
            break

ydl_opts = {
'format': 'bestaudio/best',
'outtmpl': SITE_ROOT + '/Audios/%(title)s.%(ext)s',
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'wav',
    'preferredquality': '192',
}],
}

while time.time() < timeout_start + timeout:
    if len(URLs) == 0:
        break
    print(time.time())
    N = str(choice(URLs))
    URLs.remove(N)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com' + N])
    print('\nDownloaded :', 'https://www.youtube.com' + N, '\n')
    
    time.sleep(3)
    