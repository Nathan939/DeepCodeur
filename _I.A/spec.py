import matplotlib.pyplot as plot
from scipy import signal
from scipy.io import wavfile
from pydub import AudioSegment
from glob import glob
import numpy as np
import os
import pylab
from PIL import Image
import wave
import time
import math

def wavfiles2spec():
    hotwords = [x[0] for x in os.walk('data\enregistrement\\')]
    hotwords.pop(0)

    def graph_spectrogram(wav_file, destination):
        sound_info, frame_rate = get_wav_info(wav_file)
        pylab.figure(num=None, figsize=(19, 12))
        pylab.subplot(111)
        pylab.specgram(sound_info, Fs=frame_rate)
        pylab.axis('off')
        pylab.savefig(destination, format='png', bbox_inches='tight')
    def get_wav_info(wav_file):
        wav = wave.open(wav_file, 'r')
        frames = wav.readframes(-1)
        sound_info = pylab.fromstring(frames, 'Int16')
        frame_rate = wav.getframerate()
        wav.close()
        return sound_info, frame_rate


    for files in hotwords:
        try:
            os.makedirs("data/monos/" + files.split("\\")[-1])
        except OSError:
            print("Couldn't create directorie")

        try:
            os.makedirs("data/specto/" + files.split("\\")[-1])
        except OSError:
            print("Couldn't create directorie")

        audio_files = glob(files + '/*.wav')
        for audio in audio_files:
            sound = AudioSegment.from_wav(audio)
            sound = sound.set_channels(1)
            new_audio_path = "data/monos/" + files.split("\\")[-1] + '/' + audio.split('\\')[-1]
            sound.export(new_audio_path, format="wav")

            name_file = ("data/specto/" + files.split("\\")[-1] + '/' + audio.split('\\')[-1]).replace(".wav", ".jpg")
            # graph_spectrogram(new_audio_path, name_file)
            
            # Read the wav file (mono)
            samplingFrequency, signalData = wavfile.read(new_audio_path)

            # Plot the signal read from wav file
            #plot.figure(num=None, figsize=(19, 12))
            plot.specgram(signalData,Fs=samplingFrequency)
            plot.axis('off')
            plot.savefig(name_file, format='jpg', bbox_inches='tight', dpi=200)
            print("Exported", name_file)

def get_batch(batchsize):
    directorie = "data/specto/"
    all_f = os.listdir(directorie)
    labels = {}
    images_all = []
    bat_img = []
    for labs in all_f:
        labels[labs] = all_f.index(labs)
        for fs in os.listdir(directorie + labs + "/"):
            img = Image.open(directorie + labs + "/" + fs)
            arr = np.array(img)
            images_all.append((arr, labels[labs]))

    for i in range(math.ceil(len(images_all)/batchsize)):
        bat_img.append(images_all[i*batchsize:(i+1)*batchsize])
    return bat_img


class Spec(object):
    
    def __init__(self, batchsize=1):
        self.batchsize = batchsize
        self.batches = get_batch(batchsize)
