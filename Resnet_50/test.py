# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from Parameter import Parameters
import numpy as np
import keras
import argparse
import imutils
import cv2

norm_size = 224
import threading

class AI_Test(object):

    _instance_lock=threading.Lock()

    def __init__(self):
        import time
        time.sleep(1)
        print("[INFO] loading network...")
        keras.backend.clear_session()
        self.model = load_model(Parameters.model_path)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(AI_Test, "_instance"):
            with AI_Test._instance_lock:
                if not hasattr(AI_Test, "_instance"):
                    AI_Test._instance = AI_Test(*args, **kwargs)
        return AI_Test._instance


    def predict(self,filepath):
        # load the trained convolutional neural network


        #load the image
        image = cv2.imread(filepath)

        # pre-process the image for classification
        image = cv2.resize(image, (norm_size, norm_size))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)


        # classify the input image
        result = self.model.predict(image)[0]
        #print (result.shape)
        proba = np.max(result)
        label = str(np.where(result==proba)[0])
        label = label.replace("[","").replace("]","").zfill(3)

        for key in Parameters.object_map:
            if(label in key):
                label=Parameters.object_map[key];
                break
        label = "{}: {:.2f}%".format(label, proba * 100)
        print(label)

        return label

