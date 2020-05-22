import requests
from bs4 import BeautifulSoup
import youtube_dl
import time

HOTWORD = ['minecraft', 'Minecraft', 'MINECRAFT'] # Topics you want to search
NB_OF_VID = 5 # Number of vids

videos = []

url = 'https://www.youtube.com/'

while(len(videos) < NB_OF_VID):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        liens = soup.findAll("a", {"class": "yt-uix-tile-link"})

        for link in liens:
            for mot in HOTWORD:
                if mot in link.get('title') and link.get('title') not in videos:
                    videos.append([link.get('title'), 'https://www.youtube.com/' + link.get('href')])
                    print(videos)
        time.sleep(2)
    print('Encore une fois')

print([print(vid) for vid in videos])
    