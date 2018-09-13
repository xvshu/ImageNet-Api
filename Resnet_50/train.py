# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
from keras.callbacks import TensorBoard
import numpy as np
import argparse
import random
import cv2
import os
import sys
from Resnet_50.Resnet50 import ResnetBuilder
from keras.optimizers import SGD
from Parameter import img_file_path
from Parameter import Parameters
sys.path.append('..')



def args_parse():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-dtest", "--dataset_test", default=img_file_path.File_Test,
                    help="path to input dataset_test")
    ap.add_argument("-dtrain", "--dataset_train", default=img_file_path.File_Train,
                    help="path to input dataset_train")
    ap.add_argument("-m", "--model", default=Parameters.model_path,
                    help="path to output model")
    ap.add_argument("-p", "--plot", type=str, default="plot.png",
                    help="path to output accuracy/loss plot")
    args = vars(ap.parse_args())
    return args


# initialize the number of epochs to train for, initial learning rate,
# and batch size
EPOCHS = 500
INIT_LR = 1e-3
BS = 10
CLASS_NUM = 6
norm_size = 224

def load_data(path):
    print("[INFO] loading images...")
    data = []
    labels = []
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(paths.list_images(path)))
    random.seed(42)
    random.shuffle(imagePaths)
    # loop over the input images
    for imagePath in imagePaths:
        # load the image, pre-process it, and store it in the data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (norm_size, norm_size))
        image = img_to_array(image)
        data.append(image)

        # extract the class label from the image path and update the
        # labels list
        label = int(imagePath.split(os.path.sep)[-2])
        labels.append(label)

    # scale the raw pixel intensities to the range [0, 1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # convert the labels from integers to vectors
    labels = to_categorical(labels, num_classes=CLASS_NUM)
    return data,labels

def train(aug,trainX,trainY,testX,testY,args):
    # initialize the model
    print("[INFO] compiling model...")
    model = ResnetBuilder.build_resnet_50(input_shape=[norm_size,norm_size,3], num_outputs=CLASS_NUM)
    # opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    # model.compile(loss="categorical_crossentropy", optimizer=opt,
    #               metrics=["accuracy"])
    sgd = SGD(decay=0.001,momentum=0.9)
    model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])

    # train the network
    print("[INFO] training network...")
    model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
                            validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
                            epochs=EPOCHS, verbose=1,callbacks=[TensorBoard(log_dir=Parameters.logdir)])

    # save the model to disk
    print("[INFO] serializing network...")
    model.save(args["model"])
    print("[INFO] training over")

    # plot the training loss and accuracy
    # plt.style.use("ggplot")
    # plt.figure()
    # N = EPOCHS
    # plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    # plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    # plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
    # plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
    # plt.title("Training Loss and Accuracy on traffic-sign classifier")
    # plt.xlabel("Epoch #")
    # plt.ylabel("Loss/Accuracy")
    # plt.legend(loc="lower left")
    # plt.savefig(args["plot"])

class AiResNet50(object):

    @staticmethod
    def train():
        args = args_parse()
        train_file_path = args["dataset_train"]
        test_file_path = args["dataset_test"]
        trainX,trainY = load_data(train_file_path)
        testX,testY = load_data(test_file_path)
        # construct the image generator for data augmentation
        aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                                 height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                                 horizontal_flip=True, fill_mode="nearest")
        train(aug,trainX,trainY,testX,testY,args)

# if __name__ == '__main__':
#     args = args_parse()
#     train_file_path = args["dataset_train"]
#     test_file_path = args["dataset_test"]
#     trainX,trainY = load_data(train_file_path)
#     testX,testY = load_data(test_file_path)
#     # construct the image generator for data augmentation
#     aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
#                              height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
#                              horizontal_flip=True, fill_mode="nearest")
#     train(aug,trainX,trainY,testX,testY,args)



