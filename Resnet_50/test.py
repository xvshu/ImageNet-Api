# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2

norm_size = 299

def args_parse():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model",default="D:\\Data\\ai\\model\\traffic_sign.model",
                    help="path to trained model model")
    ap.add_argument("-i", "--image",default="D:\\Data\\ai\\lenet\\img\\001.jpg",
                    help="path to input image")
    ap.add_argument("-s", "--show", action="store_true",
                    help="show predict image",default=True)
    args = vars(ap.parse_args())
    return args


def predict(args,filepath):
    # load the trained convolutional neural network
    print("[INFO] loading network...")
    model = load_model(args["model"])

    #load the image
    image = cv2.imread(filepath)
    orig = image.copy()

    # pre-process the image for classification
    image = cv2.resize(image, (norm_size, norm_size))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # classify the input image
    result = model.predict(image)[0]
    #print (result.shape)
    proba = np.max(result)
    label = str(np.where(result==proba)[0])
    label = "{}: {:.2f}%".format(label, proba * 100)
    print(label)
    return label

class AiResNet50Predict(object):
    @staticmethod
    def predict(filepath):
        args = args_parse()
        predict(args=args,filepath=filepath)