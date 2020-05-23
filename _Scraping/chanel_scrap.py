import requests
from bs4 import BeautifulSoup
import youtube_dl
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import time

hotwords = [x[0].split("\\")[-1] for x in os.walk('_I.A\Data\Enregistrement_vocal\HTML')]

NB_OF_VID = 20 # Number of vids

videos = []

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

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
    
    sound_file = AudioSegment.from_wav(AudioPath + '/' + nom + '.wav')
    
    try:
        audio_chunks = split_on_silence(sound_file, 
            # must be silent for at least half a second
            min_silence_len=500, 

            # consider it silent if quieter than -16 dBFS
            silence_thresh=-16
        )
    except UnboundLocalError:
        print('\nBad audio')

    for i, chunk in enumerate(audio_chunks):
        out_file = AudioPath + "//chunk{0}.wav".format(i)
        print ("exporting"), out_file
        chunk.export(out_file, format="wav")

downoload_audio('/watch?v=T5yquPjCSFA', "Covid-19 l'Amérique latine, nouvel épicentre de la pandémie, selon l'OMS")

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
