import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "testAudio/test.wav")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

try:
    print(r.recognize_google(audio, language="fr-fr", key="31a5e855f751a62fd6b36ab22ff8df379f867379"))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))