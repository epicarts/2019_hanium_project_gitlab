from tensorflow.keras.models import load_model
import tensorflow as tf

classifierLoad = tf.keras.models.load_model('model/sequential_4_ft.h5')
classifierLoad(img)
