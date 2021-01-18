# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 11:23:08 2020

@author: 00ery
"""
#LIBRARIES
import numpy as np
import keras

#IMPORTING DATA
(train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

#SETTING UP NETWORK
network = keras.models.Sequential()
network.add(keras.layers.Dense(512, activation='relu', input_shape=(28*28,)))
network.add(keras.layers.Dense(10, activation='softmax'))
#THE COMPILATION STEP
network.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

#PREPARING THE IMAGES
train_images = train_images.reshape((60000,28*28))
train_images = train_images.astype('float32')/255

test_images = test_images.reshape((10000,28*28))
test_images = test_images.astype('float32')/255

#PREPARING THE LABELS
train_labels = keras.utils.to_categorical(train_labels)
test_labels = keras.utils.to_categorical(test_labels)

#TRAINING
network.fit(train_images, train_labels, epochs=2, batch_size=128, verbose=0)

#PREDICTING
print(network.predict(np.array([test_images[4]])))







