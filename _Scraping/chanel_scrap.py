import requests
from bs4 import BeautifulSoup
import youtube_dl
from pydub import AudioSegment
import os
import time

hotwords = [x[0].split("\\")[-1] for x in os.walk('_I.A\Data\Enregistrement_vocal\HTML')]

NB_OF_VID = 20 # Number of vids

videos = []

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

chunk1 = 1 * 1000
chunk2 = 5 * 1000
chunk3 = 8 * 1000
chunk4 = 10 * 1000
chunk5 = 12 * 1000

def downoload_audio(url, nom):
    AudioPath = SITE_ROOT + '/Audios/' + nom
    try:
        os.makedirs(AudioPath)
    except OSError:
        print("Couldn't create directorie")

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': AudioPath + '/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com" + url])
    print('\nDownloaded :', url, '\n')

    sound = AudioSegment.from_file(AudioPath + '/' + nom + '.wav')

    for i in range(1, 5):
        splited_audio = sound[globals()['chunk' + str(i)]:globals()['chunk' + str(i+1)]] 
        splited_audio.export(AudioPath + '\\' + nom + str(i) + '.wav', format="wav")

i = 0

while(len(videos) < NB_OF_VID):
    url = "https://www.youtube.com/user/YTlanguages/search?query=" + hotwords[i]
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        liens = soup.findAll("a", {"class": "yt-uix-tile-link"})

        if len(liens) > 0:
            videos.append(liens[0].get('href'))
            downoload_audio(liens[0].get('href'), liens[0].get('title'))
            print(liens[0].get('title'), hotwords[i])

        i += 1
        time.sleep(1)
