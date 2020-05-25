from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (NoTranscriptFound, TranscriptsDisabled)
import youtube_dl
from pydub import AudioSegment
import requests
from bs4 import BeautifulSoup
import os
import time

audios_all = []
NB_AUDIOS = 50 # Nombre d'audios voulus

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

dic = {'A la ligne', 'Abreviation', 'Ajoute', 'Barre de progression', 'Bouton', 'Carte', 'Case', 'Cellule', 'Citaton','Code', 'Dans un cadre', 'Definition', 'Description', 'Ecris', 'Egal', 'En grand', 'En gras', 'Enregistrement', 'Entre', 'Fichier Audio', 'Formulaire', 'Groupe', 'Image', 'Implemente', 'Item', 'Legende', 'Lien', 'Liste a puce', 'Liste deroulante', 'Liste ordonee', 'Longue citation', 'Marque', 'Mettre en emphase', 'Objet', 'Paragraphe', 'Photo', 'Plug-in', 'Qui se diferencie', 'Redirection', 'Reduis', 'Regroupe', 'Retour a la ligne', 'Script', 'Sortie', 'Sous fenetre', 'Surligne', 'Tableau', 'Temps', 'Titre', 'Variable', 'Video'}

def video_suivante(video_id, transcribe):
    url = "https://www.youtube.com/watch?v=" + video_id
    response = requests.get(url)
    interesting_words = False
    if response.ok:
        for text in transcribe:
            for word in dic:
                if word in text['text']:
                    interesting_words = True
                    break

        if interesting_words == True:
            audio_path = SITE_ROOT + '/Audios/' + video_id

            ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': audio_path + '/' + video_id + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            }

            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print('\nDownloaded :', url, '\n')

            sound = AudioSegment.from_wav(str(audio_path) + '/' + video_id + ".wav")
            for text in transcribe:
                for word in dic:
                        if word in text['text']:
                            print('Found word')
                            debut = text['start'] * 1000
                            fin = debut + text['duration'] * 1000
                            duree = sound[debut:fin]
                            duree.export(audio_path + '/' + video_id + str(debut) + ' - subtitle : {0}.wav'.format(word), format='wav')
        else:
            print("Mais il n'y a pas les mots qui nous intéressent")

while len(audios_all) < NB_AUDIOS:
    url_yt = 'https://www.youtube.com'
    response = requests.get(url_yt)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        liens = soup.findAll("a", {"class": "yt-ui-ellipsis"})

        for link in liens:
            try:
                video_id = link.get('href').split("=")[-1]
                
                transcript = YouTubeTranscriptApi.get_transcript(video_id, ['fr'])
                print("Cette vidéo a des sous-titres en français")

                video_suivante(video_id, transcript)

                audios_all.append(link)
            except (NoTranscriptFound, TranscriptsDisabled):
                print("No subtitle")
    print("Et encore un tour !")
    time.sleep(2)               
                    