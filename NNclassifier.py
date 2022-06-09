import numpy as np 
import pandas as pd

import os
dir_black = os.path.join('./Soil types trainset/[Loamy] Black Soil')
dir_Laterite = os.path.join('./Soil types trainset/[Clay] Laterite Soil')
dir_peat = os.path.join('./Soil types trainset/[Sandy Loam] Peat Soil')
dir_yellow = os.path.join('./Soil types trainset/[Sandy] Yellow Soil')

import tensorflow as tf
from tensorflow import keras

image_size = 220
batch_size = 15


target_size = (image_size, image_size)
input_shape = (image_size, image_size, 3)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rotation_range=20,
		zoom_range=0.15,
		width_shift_range=0.2,
		height_shift_range=0.2,
		shear_range=0.15,
		horizontal_flip=True,
		fill_mode="nearest")


train_generator = train_datagen.flow_from_directory(
        './Soil types trainset/', 
        target_size=(220, 220),
        batch_size = batch_size,
        classes = [ '[Clay] Laterite Soil', '[Loamy] Black Soil', '[Sandy Loam] Peat Soil','[Sandy] Yellow Soil'],
       class_mode='categorical')



print(train_generator.class_indices)

model = tf.keras.models.Sequential([
    
    # The first convolution
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(220, 220, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The third convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The fourth convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The fifth convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
    # Flatten the results to feed into a dense layer
    tf.keras.layers.Flatten(),
    # 128 neuron in the fully-connected layer
    tf.keras.layers.Dense(128, activation='relu'),
    # 5 output neurons for 5 classes with the softmax activation
    tf.keras.layers.Dense(4, activation='softmax')
])

model.summary()

from keras.optimizers import RMSprop

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(learning_rate=0.001),
              metrics=['acc'])

total_sample = train_generator.n
n_epochs = 30

history = model.fit(
        train_generator, 
        steps_per_epoch = int(total_sample/batch_size),  
        epochs = n_epochs,
        verbose = 1)

import matplotlib.pyplot as plt
plt.figure(figsize=(7,4))
plt.plot([i+1 for i in range(n_epochs)],history.history['acc'],'-o',c='k',lw=1,markersize=2)
plt.grid(True)
plt.title("Training accuracy with epochs\n")
plt.xlabel("Training epochs")
plt.ylabel("Training accuracy")
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.show()

model.save('my_model.h5')
model.save(filepath="save_model/")

from keras.models import Sequential
model.export(export_dir='.')

converter = tf.lite.TFLiteConverter.from_saved_model('save_model')
tflite_model = converter.convert()
open("soil.tflite", "wb").write(tflite_model)

model.save_weights("model.h5")