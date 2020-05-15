#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import os

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Google Cloud Speech
GOOGLE_CLOUD_SPEECH_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
with open(GOOGLE_CLOUD_SPEECH_CREDENTIALS, 'r') as file:
    json_cred = file.read()
try:
    print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=json_cred, language="fr-FR"))
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))
