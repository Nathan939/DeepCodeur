import requests
from bs4 import BeautifulSoup
import youtube_dl
import time
import os.path

"""
links = []

for i in range(2):
    url = 'http://example.webscraping.com/places/default/index/' + str(i)
    response = requests.get(url)
    print(response)
    if response.ok:
        print('Page: ' + str(i))
        soup = BeautifulSoup(response.text, 'lxml')
        tds = soup.findAll('td')
        for td in tds:
            a = td.find('a')
            link = a['href']
            links.append('http://example.webscraping.com/' + link)
        time.sleep(3)

print(len(links))

with open('urls.txt', 'w') as file:
    for link in links:
        file.write(link + '\n')

with open('urls.txt', 'r') as inf:
    with open('pays.csv', 'w') as outf:
        outf.write('pays, population\n')
        for row in inf:
            url = row.strip()
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.text, 'lxml')
                country = soup.find('tr', {'id' : 'places_country__row'}).find('td', {'class': 'w2p_fw'})
                pop = soup.find('tr', {'id' : 'places_population__row'}).find('td', {'class': 'w2p_fw'})
                print('Pays: ' + country.text + ', Pop: ' + pop.text)
                outf.write(country.text + ',' + pop.text.replace(',', '') + '\n')
            time.sleep(3)
"""
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
"""
url = 'http://localhost:8000/static/blog/image/RedAndBlack.png'
response = requests.get(url)

def downloadFile(AFileName):
    # extract file name from AFileName
    filename = SITE_ROOT + '/Audios/' + AFileName.split("/")[-1] 
    # download image using GET
    rawImage = requests.get(AFileName, stream=True)
    # save the image recieved into the file
    with open(filename, 'wb') as fd:
        for chunk in rawImage.iter_content(chunk_size=1024):
            fd.write(chunk)
        print("Downloaded :",  AFileName.split("/")[-1], "from", AFileName)
    return

#downloadFile("http://localhost:8000/static/blog/audios/test.wav")
"""
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
    ydl.download(['https://www.youtube.com/watch?v=ACPVLkRzSN0'])
