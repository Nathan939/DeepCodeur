from youtube_transcript_api import YouTubeTranscriptApi
from pydub import AudioSegment
import io 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import requests
from bs4 import BeatifulSoup

transcribe = YouTubeTranscriptApi.get_transcript("f98j2fwJykc", languages=['fr', 'fr'])

dic = {'A la ligne', 'Abreviation', 'Ajoute', 'Barre de progression', 'Bouton', 'Carte', 'Case', 'Cellule', 'Citaton','Code', 'Dans un cadre', 'Definition', 'Description', 'Ecris', 'Egal', 'En grand', 'En gras', 'Enregistrement', 'Entre', 'Fichier Audio', 'Formulaire', 'Groupe', 'Image', 'Implemente', 'Item', 'Legende', 'Lien', 'Liste a puce', 'Liste deroulante', 'Liste ordonee', 'Longue citation', 'Marque', 'Mettre en emphase', 'Objet', 'Paragraphe', 'Photo', 'Plug-in', 'Qui se diferencie', 'Redirection', 'Reduis', 'Regroupe', 'Retour a la ligne', 'Script', 'Sortie', 'Sous fenetre', 'Surligne', 'Tableau', 'Temps', 'Titre', 'Variable', 'Video'}

for text in transcribe[0]:
       for word in text['text']:
            if word in dic:
                five_seconds = 5 * 1000
                debut = song[ten_seconds]
                fin = song[-5000:]
                duree = sound[int(début):int(fin)]
                export = sound.export('subtitle', wav)

                stop_words = set(stopwords.words('french')) 
                file1 = open("frenchST.txt") 
                line = file1.read()
                words = line.split() 
                for r in words: 
                    if not r in stop_words: 
                        appendFile = open('filteredtext.txt','a') 
                        appendFile.write(" "+r) 
                        appendFile.close() 
                def video_suivante():
                    url = 'https://www.youtube.com/watch?v=dRxh6pBEvSw'
                    response = requests.get(url)
                    if response.ok:
                        soup = BeatifulSoup(response.txt, 'lxml')
                        title = soup.find('a')
                        title = int(title)
                        random.random(title)
            
            elif word = False:
                def video_suivante():
                    pass

            else:
                def video_suivante():
                    pass
 
                



                
                    