import tensorflow as tf
from tensorflow import keras

import numpy as np

model = keras.models.load_model('my_model.h5')

def NNpredict(filepath, model=model):
# load and resize image to 200x200
    test_image = tf.keras.preprocessing.image.load_img(filepath,
                            target_size=(220,220))
    # convert image to numpy array
    images = tf.keras.preprocessing.image.img_to_array(test_image)
    # expand dimension of image
    images = np.array([images])

    prediction = model.predict(images)
    return prediction