from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from load_images import MoleImages
import matplotlib.pyplot as plt
import sys
import tensorflow as tf
from skimage import io
from skimage.transform import resize

if __name__ == '__main__':
    global model
    global graph
    model = load_model('model.h5')
    graph = tf.get_default_graph()
    mimg = MoleImages()
    X = io.imread("./ISIC_0000001.jpeg")
    img = resize(X, (128,128), mode='constant') * 255
    if img.shape[2] == 4:
        img = img[:,:,0:3]
        print (img.shape)
    
    with graph.as_default():
        y_pred = model.predict(img)[0:0]
        print(y_pred,type(y_pred))

        if y_pred > 0.9:
            result = 'High Risk'
            print(result)
        elif (y_pred <= 0.9 and y_pred > 0.5):
            result = 'Medium Risk'
            print(result)
        else:
            result = 'Low Risk'
            X_test, y_test = mimg.load_test_images('data_test/benign/images',
                                                'data_test/malign/images')
            # model = load_model('model_weights.h5')
            y_pred_proba = model.predict(X_test)
            y_pred = (y_pred_proba >0.5)*1
            # print(classification_report(y_test,y_pred))
            # plot_roc(y_test, y_pred_proba, title=sys.argv[1]+sys.argv[2])


