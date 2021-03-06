import librosa as lr
import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from zipfile import ZipFile 
import imgaug as ia
import imgaug.augmenters as iaa


def decompresseur():
    # spécifiant le nom du fichier zip
    file = "archive.zip"

    # ouvrir le fichier zip en mode lecture
    with ZipFile(file, 'r') as zip: 
        # extraire tous les fichiers vers un autre répertoire
        zip.extractall('zip_destination')

    y, sr = lr.load(lr.util.example_audio_file())
    lr.feature.mfcc(y=None, sr=22050, S=None, n_mfcc=20, dct_type=2, norm='ortho', lifter=0, **kwargs)


def wav2spectrum():
    data_dir = './Data/Enregistrement_vocal/HTML'
    audio_files = glob(data_dir + '/*.wav')

    audio, sfreq = lr.load(audio_files[7]) #element variable
    time = np.arange(0, len(audio)) / sfreq

    fig, ax = plt.subplots()
    ax.plot(time, audio)
    ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')
    plt.show()

    for file in range(0, len(audio_files), 1):
        audio, sfreq = lr.load(audio_files[file]) #element variable
        time = np.arange(0, len(audio)) / sfreq

        fig, ax = plt.subplots()
        ax.plot(time, audio)
        ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')
        # random example images
        images = plt.show()

        # Sometimes(0.5, ...) applies the given augmenter in 50% of all cases,
        # e.g. Sometimes(0.5, GaussianBlur(0.3)) would blur roughly every second image.
        sometimes = lambda aug: iaa.Sometimes(0.5, aug)

        # Define our sequence of augmentation steps that will be applied to every image
        # All augmenters with per_channel=0.5 will sample one value _per image_
        # in 50% of all cases. In all other cases they will sample new values
        # _per channel_.

        seq = iaa.Sequential(
            [
                # apply the following augmenters to most images
                iaa.Fliplr(0.5), # horizontally flip 50% of all images
                iaa.Flipud(0.2), # vertically flip 20% of all images
                # crop images by -5% to 10% of their height/width
                sometimes(iaa.CropAndPad(
                    percent=(-0.05, 0.1),
                    pad_mode=ia.ALL,
                    pad_cval=(0, 255)
                )),
                sometimes(iaa.Affine(
                    scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}, # scale images to 80-120% of their size, individually per axis
                    translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}, # translate by -20 to +20 percent (per axis)
                    rotate=(-45, 45), # rotate by -45 to +45 degrees
                    shear=(-16, 16), # shear by -16 to +16 degrees
                    order=[0, 1], # use nearest neighbour or bilinear interpolation (fast)
                    cval=(0, 255), # if mode is constant, use a cval between 0 and 255
                    mode=ia.ALL # use any of scikit-image's warping modes (see 2nd image from the top for examples)
                )),
                # execute 0 to 5 of the following (less important) augmenters per image
                # don't execute all of them, as that would often be way too strong
                iaa.SomeOf((0, 5),
                    [
                        sometimes(iaa.Superpixels(p_replace=(0, 1.0), n_segments=(20, 200))), # convert images into their superpixel representation
                        iaa.OneOf([
                            iaa.GaussianBlur((0, 3.0)), # blur images with a sigma between 0 and 3.0
                            iaa.AverageBlur(k=(2, 7)), # blur image using local means with kernel sizes between 2 and 7
                            iaa.MedianBlur(k=(3, 11)), # blur image using local medians with kernel sizes between 2 and 7
                        ]),
                        iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)), # sharpen images
                        iaa.Emboss(alpha=(0, 1.0), strength=(0, 2.0)), # emboss images
                        # search either for all edges or for directed edges,
                        # blend the result with the original image using a blobby mask
                        iaa.SimplexNoiseAlpha(iaa.OneOf([
                            iaa.EdgeDetect(alpha=(0.5, 1.0)),
                            iaa.DirectedEdgeDetect(alpha=(0.5, 1.0), direction=(0.0, 1.0)),
                        ])),
                        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5), # add gaussian noise to images
                        iaa.OneOf([
                            iaa.Dropout((0.01, 0.1), per_channel=0.5), # randomly remove up to 10% of the pixels
                            iaa.CoarseDropout((0.03, 0.15), size_percent=(0.02, 0.05), per_channel=0.2),
                        ]),
                        iaa.Invert(0.05, per_channel=True), # invert color channels
                        iaa.Add((-10, 10), per_channel=0.5), # change brightness of images (by -10 to 10 of original value)
                        iaa.AddToHueAndSaturation((-20, 20)), # change hue and saturation
                        # either change the brightness of the whole image (sometimes
                        # per channel) or change the brightness of subareas
                        iaa.OneOf([
                            iaa.Multiply((0.5, 1.5), per_channel=0.5),
                            iaa.FrequencyNoiseAlpha(
                                exponent=(-4, 0),
                                first=iaa.Multiply((0.5, 1.5), per_channel=True),
                                second=iaa.LinearContrast((0.5, 2.0))
                            )
                        ]),
                        iaa.LinearContrast((0.5, 2.0), per_channel=0.5), # improve or worsen the contrast
                        iaa.Grayscale(alpha=(0.0, 1.0)),
                        sometimes(iaa.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25)), # move pixels locally around (with random strengths)
                        sometimes(iaa.PiecewiseAffine(scale=(0.01, 0.05))), # sometimes move parts of the image around
                        sometimes(iaa.PerspectiveTransform(scale=(0.01, 0.1)))
                    ],
                    random_order=True
                )
            ],
            random_order=True
        )
        images_aug = seq(images=images)

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