from django.shortcuts import render
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime
from django.shortcuts import render
from _Tests import audio_transcribe

# Pour savugerder l'audio
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import speech_recognition as sr

def index(request):
    template = loader.get_template('blog/index.html')
    return HttpResponse(template.render(request=request))

def envoi(request):
    audio_data = request.body
    default_storage.delete('audio/' + 'test' + '.wav')
    path = default_storage.save('audio/' + 'test' + '.wav', ContentFile(audio_data))
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    # Google Cloud Recognition
    try:
        result = r.recognize_google(audio, language="fr-fr", key="31a5e855f751a62fd6b36ab22ff8df379f867379")
    except sr.UnknownValueError:
        result = "JE N'AI PAS COMPRIS"
    """
    # Pocket Sphinx
    try:
        result = r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        result = "JE N'AI PAS COMPRIS"
    """
    print(result)
    # Crer un fichier txt avec le résultat de l'enregistrement
    f = open("resultat.txt", "w+")
    f.write(result.replace(' ', '\n'))
    f.close()
    return HttpResponse(result)