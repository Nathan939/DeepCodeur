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
    with open("google-api-key.json", 'r') as file:
            json_cred = file.read()
    try:
        result = r.recognize_google_cloud(audio, credentials_json=json_cred, language="fr-FR")
    except sr.UnknownValueError:
        result = "JE N'AI PAS COMPRIS"
    # Pocket Sphinx
    """try:
        result = r.recognize_sphinx(audio, language="fr-FR")
    except sr.UnknownValueError:
        result = "JE N'AI PAS COMPRIS" """
    print(result)
    return HttpResponse(result)