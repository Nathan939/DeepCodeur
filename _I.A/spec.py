import matplotlib.pyplot as plot
from scipy import signal
from scipy.io import wavfile
from pydub import AudioSegment
from glob import glob

data_dir = 'data/enregistrement'
audio_files = glob(data_dir + '/temps' + '/*.wav')

for files in audio_files:
    sound = AudioSegment.from_wav(files)
    sound = sound.set_channels(1)
    sound.export("data/enregistrement/monos/" + files.split('\\')[-1], format="wav")

audio_files = glob(data_dir + '/monos' + '/*.wav')

for files in audio_files:
    # Read the wav file (mono)
    samplingFrequency, signalData = wavfile.read(files)

    # Plot the signal read from wav file
    plot.specgram(signalData,Fs=samplingFrequency)
    plot.axis('off')
    name_file = files.split("\\")[-1].replace(".wav", ".png")
    plot.savefig("data/enregistrement/specto/" + name_file, format='png')