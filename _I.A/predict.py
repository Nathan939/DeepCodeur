from cifar import Cifar
from spec import Spec
import tensorflow as tf
import AlexNet
import helper

sp = Spec(batch_size=16)

src_img = sp.batches[0]

with tf.Session() as sess:

    