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
from random import choices

def wavfiles2spec():
    hotwords = [x[0] for x in os.walk('data\enregistrement\\')]
    hotwords.pop(0)

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
            plot.figure(figsize=(9.04, 5.98), dpi=100)
            plot.specgram(signalData,Fs=samplingFrequency)
            plot.axis('off')
            plot.savefig(name_file, format='jpg', bbox_inches='tight')
            print("Exported", name_file)
            plot.close('all')


def get_batch(batchsize, wanna_batch):
    directorie = "data/specto/"
    all_f = os.listdir(directorie)
    labels = {}
    images_all = []
    bat_img = []
    for labs in all_f:
        labels[labs] = all_f.index(labs)
        for fs in os.listdir(directorie + labs + "/"):
            img = Image.open(directorie + labs + "/" + fs)
            im = img.resize((32, 32))
            arr = np.array(im)
            images_all.append((arr, labels[labs]))

    for i in range(math.ceil(len(images_all)/batchsize)):
        bat_img.append(images_all[i*batchsize:(i+1)*batchsize])
    if wanna_batch:
        return bat_img
    else:
        return images_all


class Spec(object):
    
    def __init__(self, batch_size=1):
        self.batch_size = batch_size
        self.batches = get_batch(batch_size, True)
        self.test_set = choices(get_batch(1, False), k=math.ceil(len(get_batch(1, False)) / 5))