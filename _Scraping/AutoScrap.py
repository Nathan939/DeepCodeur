import requests
from bs4 import BeautifulSoup
import time
from random import *
import os.path
import youtube_dl
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi
import wave
import contextlib
from math import *

def get_audio_length(path_audio):
    with contextlib.closing(wave.open(path_audio,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration
    
def supp_stop_words(string404):
    file1 = open("frenchST.txt")
    line = file1.read()
    mots = line.split()
    for r in string404:
        if r in mots:
            string404.remove(r)
    return string404

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
audio_path = os.path.join(SITE_ROOT, 'Audios\BpRYULlk5H4\BpRYULlk5H4.wav')
sound = AudioSegment.from_wav(audio_path)
transcript = YouTubeTranscriptApi.get_transcript("BpRYULlk5H4", ['fr'])

texte = transcript[0]['text'].split()
chunks_size = ceil(get_audio_length(audio_path) / 100) * 100 / len(texte)
removed_list = supp_stop_words(texte)    

print(transcript[0]['start'], transcript[0]['start'] + transcript[0]['duration'], transcript[0]['start'] + transcript[0]['duration'] / len(texte))

chunks_size = (transcript[0]['start'] + transcript[0]['duration'] / len(texte)) * 1000

for ch in range(0, len(removed_list)):
    part = sound[ch * chunks_size:(ch + 1) * chunks_size]
    part.export('Audios/youpi {0}.wav'.format(ch), format='wav')
