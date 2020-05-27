<<<<<<< Updated upstream
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
=======
import tensorflow as tf

n_classes = 10 # <-- newly added constant 

image_size = 32
input_images = tf.placeholder(tf.float32,
                              shape=[None, image_size, image_size, 3], 
                              name="input_images")

# First CONV layer
kernel = tf.Variable(tf.truncated_normal([11, 11, 3, 96],
                                         dtype=tf.float32,
                                         stddev=1e-1),
                     name="conv1_weights")
conv = tf.nn.conv2d(input_images, kernel, [1, 4, 4, 1], padding="SAME")
bias = tf.Variable(tf.truncated_normal([96]))
conv_with_bias = tf.nn.bias_add(conv, bias)
conv1 = tf.nn.relu(conv_with_bias, name="conv1")

lrn1 = tf.nn.lrn(conv1,
                 alpha=1e-4,
                 beta=0.75,
                 depth_radius=2,
                 bias=2.0)

pooled_conv1 = tf.nn.max_pool(lrn1,
                              ksize=[1, 3, 3, 1],
                              strides=[1, 2, 2, 1],
                              padding="SAME",
                              name="pool1")

# Second CONV Layer 
kernel = tf.Variable(tf.truncated_normal([5, 5, 96, 256],
                                         dtype=tf.float32,
                                         stddev=1e-1),
                     name="conv2_weights")
conv = tf.nn.conv2d(pooled_conv1, kernel, [1, 4, 4, 1], padding="SAME")
bias = tf.Variable(tf.truncated_normal([256]), name="conv2_bias")
conv_with_bias = tf.nn.bias_add(conv, bias)
conv2 = tf.nn.relu(conv_with_bias, name="conv2")
lrn2 = tf.nn.lrn(conv2,
                 alpha=1e-4,
                 beta=0.75,
                 depth_radius=2,
                 bias=2.0)

pooled_conv2 = tf.nn.max_pool(lrn2,
                              ksize=[1, 3, 3, 1],
                              strides=[1, 2, 2, 1],
                              padding="SAME",
                              name="pool2")

# Third CONV layer
kernel = tf.Variable(tf.truncated_normal([3, 3, 256, 384],
                                         dtype=tf.float32,
                                         stddev=1e-1),
                     name="conv3_weights")
conv = tf.nn.conv2d(pooled_conv2, kernel, [1, 1, 1, 1], padding="SAME")
bias = tf.Variable(tf.truncated_normal([384]), name="conv3_bias")
conv_with_bias = tf.nn.bias_add(conv, bias)
conv3 = tf.nn.relu(conv_with_bias, name="conv3")

# Fourth CONV layer
kernel = tf.Variable(tf.truncated_normal([3, 3, 384, 384],
                                         dtype=tf.float32,
                                         stddev=1e-1),
                     name="conv4_weights")
conv = tf.nn.conv2d(conv3, kernel, [1, 1, 1, 1], padding="SAME")
bias = tf.Variable(tf.truncated_normal([384]), name="conv4_bias")
conv_with_bias = tf.nn.bias_add(conv, bias)
conv4 = tf.nn.relu(conv_with_bias, name="conv4")

# Fifth CONV Layer
kernel = tf.Variable(tf.truncated_normal([3, 3, 384, 256],
                                         dtype=tf.float32,
                                         stddev=1e-1),
                     name="conv5_weights")
conv = tf.nn.conv2d(conv4, kernel, [1, 1, 1, 1], padding="SAME")
bias = tf.Variable(tf.truncated_normal([256]), name="conv5_bias")
conv_with_bias = tf.nn.bias_add(conv, bias)
conv5 = tf.nn.relu(conv_with_bias, name="conv5")

# Fully Connected Layers
fc_size = 256
conv5 = tf.layers.flatten(conv5) # tf.flatten
weights = tf.Variable(tf.truncated_normal([fc_size, fc_size]), name="fc1_weights")
bias = tf.Variable(tf.truncated_normal([fc_size]), name="fc1_bias")
fc1 = tf.matmul(conv5, weights) + bias
fc1 = tf.nn.relu(fc1, name="fc1")

weights = tf.Variable(tf.truncated_normal([fc_size, fc_size]), name="fc2_weights")
bias = tf.Variable(tf.truncated_normal([fc_size]), name="fc2_bias")
fc2 = tf.matmul(fc1, weights) + bias
fc2 = tf.nn.relu(fc2, name="fc2")

weights = tf.Variable(tf.zeros([fc_size, n_classes]), name="output_weight")
bias = tf.Variable(tf.truncated_normal([n_classes]), name="output_bias")
out = tf.matmul(fc2, weights) + bias
>>>>>>> Stashed changes
