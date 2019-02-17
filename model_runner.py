import tensorflow as tf
import os
from keras.models import load_model
from moleimages import MoleImages
import tensorflow as tf

def predict(filename):
    mimg = MoleImages()
    path_to_file = app.config['UPLOAD_FOLDER'] + '/' + filename
    X = mimg.load_image(path_to_file)
    global graph
    with graph.as_default():
        y_pred = model.predict(X)[0,0]
        print(y_pred,type(y_pred))
    if y_pred > 0.9:
        result = 'High Risk'
        print(result)
    elif (y_pred <= 0.9 and y_pred > 0.5):
        result = 'Medium Risk'
        print(result)
    else:
        result = 'Low Risk'
        print(result)


if __name__ == '__main__':
	global model
    model = load_model('models/BM_VA_VGG_FULL_DA.hdf5')
    graph = tf.get_default_graph()


