import librosa as lr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from zipfile import ZipFile 

def decompresseur():
    # spécifiant le nom du fichier zip
    file = "archive.zip"

    # ouvrir le fichier zip en mode lecture
    with ZipFile(file, 'r') as zip: 
        # extraire tous les fichiers vers un autre répertoire
        zip.extractall('zip_destination')

    y, sr = librosa.load(librosa.util.example_audio_file())
    librosa.feature.mfcc(y=None, sr=22050, S=None, n_mfcc=20, dct_type=2, norm='ortho', lifter=0, **kwargs)


def wav2spectrum():
    data_dir = './Data/Enregistrement_vocal/HTML'
    audio_files = glob(data_dir + '/*.wav')

    audio, sfreq = lr.load(audio_files[7]) #element variable
    time = np.arange(0, len(audio)) / sfreq

    fig, ax = plt.subplots()
    ax.plot(time, audio)
    ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')
    plt.show()

    %%time

    for file in range(0, len(audio_files), 1):
        audio, sfreq = lr.load(audio_files[file]) #element variable
        time = np.arange(0, len(audio)) / sfreq

        fig, ax = plt.subplots()
        ax.plot(time, audio)
        ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')
        plt.show()

def sampling():
    audio_file = './siren_mfcc_demo.wav'


    import wave
    with wave.open(audio_file, "rb") as wave_file:
        sr = wave_file.getframerate()
    print(sr)

    audio_binary = tf.read_file(audio_file)

    waveform = tf.contrib.ffmpeg.decode_audio(audio_binary, file_format='wav', samples_per_second=sr, channel_count=1)
    print(waveform.numpy().shape)

    signals = tf.reshape(waveform, [1, -1])
    signals.get_shape()

    frames = tf.contrib.signal.frame(signals, frame_length=128, frame_step=32)
    print(frames.numpy().shape)

    magnitude_spectrograms = tf.abs(tf.contrib.signal.stft(
        signals, frame_length=256, frame_step=64, fft_length=256))

    print(magnitude_spectrograms.numpy().shape)