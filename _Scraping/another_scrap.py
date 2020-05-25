import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import json
import pprint

hotwords = [x[0].split("\\")[-1] for x in os.walk('_I.A\Data\Enregistrement_vocal\HTML')]

NB_OF_VID = 20 # Number of vids

videos = []

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

transcript = YouTubeTranscriptApi.get_transcript("z0M7_HPSi14", languages=['fr', 'fr'])
parsed = json.loads(str(transcript).replace("{'", '{"').replace("':", '":').replace(" '", ' "').replace("',", '",').replace("\\x", " ").replace('\\n', " "))
f = open("transcribe.json", "w+")
f.write(json.dumps(parsed, indent=4, sort_keys=True))
f.close()

def downoload_audio(url, nom):
    nom = nom.replace('?', ' ')

    AudioPath = SITE_ROOT + '/Audios/' + nom
    try:
        os.makedirs(AudioPath)
    except OSError:
        print("Couldn't create directorie")

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': AudioPath + '/' + nom + '.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    }
    """
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com" + url])
    print('\nDownloaded :', url, '\n')
    """
    sound_file = AudioSegment.from_wav(AudioPath + '/' + nom + '.wav')

    for i in range(0, len(transcript)):
        starting = transcript[i]['start'] * 1000
        ending = starting + (transcript[i]['duration'] * 1000)
        first = sound_file[starting:ending]

        first.export(AudioPath + '/chunk{0}.wav'.format(i), format="wav")


downoload_audio('/watch?v=z0M7_HPSi14', "How do fish make electricity? - Eleanor Nelsen")