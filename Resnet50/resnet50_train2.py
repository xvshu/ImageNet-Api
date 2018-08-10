# -*- coding: utf-8 -*-
import cv2
import numpy as np
import h5py
import os

from keras.utils import np_utils, conv_utils
from keras.models import Model
from keras.layers import Flatten, Dense, Input
from keras.optimizers import Adam
from keras.applications.resnet50 import ResNet50
from keras import backend as K

def get_name_list(filepath):                #获取各个类别的名字
    pathDir =  os.listdir(filepath)
    out = []
    for allDir in pathDir:
        if os.path.isdir(os.path.join(filepath,allDir)):
            child = allDir.decode('gbk')    # .decode('gbk')是解决中文显示乱码问题
            out.append(child)
    return out

def eachFile(filepath):                 #将目录内的文件名放入列表中
    pathDir =  os.listdir(filepath)
    # out = []
    # for allDir in pathDir:
    #     child = allDir.decode('gbk')    # .decode('gbk')是解决中文显示乱码问题
    #     out.append(child)
    return pathDir

def get_data(data_name,train_left=0.0,train_right=0.7,train_all=0.7,resize=True,data_format=None,t=''):   #从文件夹中获取图像数据
    file_name = os.path.join(pic_dir_out,data_name+t+'_'+str(train_left)+'_'+str(train_right)+'_'+str(Width)+"X"+str(Height)+".h5")
    print(file_name)
    if os.path.exists(file_name):           #判断之前是否有存到文件中
        f = h5py.File(file_name,'r')
        if t=='train':
            X_train = f['X_train'][:]
            y_train = f['y_train'][:]
            f.close()
            return (X_train, y_train)
        elif t=='test':
            X_test = f['X_test'][:]
            y_test = f['y_test'][:]
            f.close()
            return (X_test, y_test)
        else:
            return
    data_format = conv_utils.normalize_data_format(data_format)
    pic_dir_set = eachFile(pic_dir_data)
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    label = 0
    for pic_dir in pic_dir_set:
        print(pic_dir_data+pic_dir)
        if not os.path.isdir(os.path.join(pic_dir_data,pic_dir)):
            continue
        pic_set = eachFile(os.path.join(pic_dir_data,pic_dir))
        pic_index = 0
        train_count = int(len(pic_set)*train_all)
        train_l = int(len(pic_set)*train_left)
        train_r = int(len(pic_set)*train_right)
        for pic_name in pic_set:
            if not os.path.isfile(os.path.join(pic_dir_data,pic_dir,pic_name)):
                continue
            img = cv2.imread(os.path.join(pic_dir_data,pic_dir,pic_name))
            if img is None:
                continue
            if (resize):
                img = cv2.resize(img,(Width,Height))
                img = img.reshape(-1,Width,Height,3)
            if (pic_index < train_count):
                if t=='train':
                    if (pic_index >= train_l and pic_index < train_r):
                        X_train.append(img)
                        y_train.append(label)
            else:
                if t=='test':
                    X_test.append(img)
                    y_test.append(label)
            pic_index += 1
        if len(pic_set) != 0:
            label += 1

    f = h5py.File(file_name,'w')
    if t=='train':
        X_train = np.concatenate(X_train,axis=0)
        y_train = np.array(y_train)
        f.create_dataset('X_train', data = X_train)
        f.create_dataset('y_train', data = y_train)
        f.close()
        return (X_train, y_train)
    elif t=='test':
        X_test = np.concatenate(X_test,axis=0)
        y_test = np.array(y_test)
        f.create_dataset('X_test', data = X_test)
        f.create_dataset('y_test', data = y_test)
        f.close()
        return (X_test, y_test)
    else:
        return

def main():
    global Width, Height, pic_dir_out, pic_dir_data
    Width = 224
    Height = 224
    num_classes = 3
    pic_dir_out = 'D:\\Data\\ai\\lenet\\out\\'
    pic_dir_data = 'D:\\Data\\ai\\lenet\\train\\'
    sub_dir = 'resnet50/'
    if not os.path.isdir(os.path.join(pic_dir_out,sub_dir)):
        os.mkdir(os.path.join(pic_dir_out,sub_dir))
    pic_dir_mine = os.path.join(pic_dir_out,sub_dir)
    (X_train, y_train) = get_data("Caltech101_color_data_",0.0,0.7,data_format='channels_last',t='train')
    y_train = np_utils.to_categorical(y_train, num_classes)

    input_tensor = Input(shape=(224, 224, 3))
    base_model = ResNet50(input_tensor=input_tensor,include_top=False,weights='imagenet')
    #base_model = ResNet50(input_tensor=input_tensor,include_top=False,weights=None)
    get_resnet50_output = K.function([base_model.layers[0].input, K.learning_phase()],
                                     [base_model.layers[-1].output])

    file_name = os.path.join(pic_dir_mine,'resnet50_train_output'+'.h5')
    if os.path.exists(file_name):
        f = h5py.File(file_name,'r')
        resnet50_train_output = f['resnet50_train_output'][:]
        f.close()
    else:
        resnet50_train_output = []
        delta = 10
        for i in range(0,len(X_train),delta):
            print(i)
            one_resnet50_train_output = get_resnet50_output([X_train[i:i+delta], 0])[0]
            resnet50_train_output.append(one_resnet50_train_output)
        resnet50_train_output = np.concatenate(resnet50_train_output,axis=0)
        f = h5py.File(file_name,'w')
        f.create_dataset('resnet50_train_output', data = resnet50_train_output)
        f.close()

    input_tensor = Input(shape=(1, 1, 2048))
    x = Flatten()(input_tensor)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    model = Model(inputs=input_tensor, outputs=predictions)
    model.compile(optimizer=Adam(), loss='categorical_crossentropy',metrics=['accuracy'])

    print('\nTraining ------------')    #从文件中提取参数，训练后存在新的文件中
    cm = 0                              #修改这个参数可以多次训练
    cm_str = '' if cm==0 else str(cm)
    cm2_str = '' if (cm+1)==0 else str(cm+1)
    if cm >= 1:
        model.load_weights(os.path.join(pic_dir_mine,'cnn_model_Caltech101_resnet50_'+cm_str+'.h5'))
    model.fit(resnet50_train_output, y_train, epochs=10, batch_size=5,)
    model.save_weights(os.path.join(pic_dir_mine,'cnn_model_Caltech101_resnet50_'+cm2_str+'.h5'))

    (X_test, y_test) = get_data("Caltech101_color_data_",0.0,0.7,data_format='channels_last',t='test')
    y_test = np_utils.to_categorical(y_test, num_classes)

    file_name = os.path.join(pic_dir_mine,'resnet50_test_output'+'.h5')
    if os.path.exists(file_name):
        f = h5py.File(file_name,'r')
        resnet50_test_output = f['resnet50_test_output'][:]
        f.close()
    else:
        resnet50_test_output = []
        delta = 10
        for i in range(0,len(X_test),delta):
            print(i)
            one_resnet50_test_output = get_resnet50_output([X_test[i:i+delta], 0])[0]
            resnet50_test_output.append(one_resnet50_test_output)
        resnet50_test_output = np.concatenate(resnet50_test_output,axis=0)
        f = h5py.File(file_name,'w')
        f.create_dataset('resnet50_test_output', data = resnet50_test_output)
        f.close()
    print('\nTesting ------------')     #对测试集进行评估
    class_name_list = get_name_list(pic_dir_data)    #获取top-N的每类的准确率
    pred = model.predict(resnet50_test_output, batch_size=32)
    f = h5py.File(os.path.join(pic_dir_mine,'pred_'+cm2_str+'.h5'),'w')
    f.create_dataset('pred', data = pred)
    f.close()

    N = 1
    pred_list = []
    for row in pred:
        pred_list.append(row.argsort()[-N:][::-1])  #获取最大的N个值的下标
    pred_array = np.array(pred_list)
    test_arg = np.argmax(y_test,axis=1)
    class_count = [0 for _ in range(num_classes)]
    class_acc = [0 for _ in range(num_classes)]
    for i in range(len(test_arg)):
        class_count[test_arg[i]] += 1
        if test_arg[i] in pred_array[i]:
            class_acc[test_arg[i]] += 1
    print('top-'+str(N)+' all acc:',str(sum(class_acc))+'/'+str(len(test_arg)),sum(class_acc)/float(len(test_arg)))
    for i in range(num_classes):
        print (i, class_name_list[i], 'acc: '+str(class_acc[i])+'/'+str(class_count[i]))

    print('----------------------------------------------------')
    N = 5
    pred_list = []
    for row in pred:
        pred_list.append(row.argsort()[-N:][::-1])  #获取最大的N个值的下标
    pred_array = np.array(pred_list)
    test_arg = np.argmax(y_test,axis=1)
    class_count = [0 for _ in range(num_classes)]
    class_acc = [0 for _ in range(num_classes)]
    for i in range(len(test_arg)):
        class_count[test_arg[i]] += 1
        if test_arg[i] in pred_array[i]:
            class_acc[test_arg[i]] += 1
    print('top-'+str(N)+' all acc:',str(sum(class_acc))+'/'+str(len(test_arg)),sum(class_acc)/float(len(test_arg)))
    for i in range(num_classes):
        print (i, class_name_list[i], 'acc: '+str(class_acc[i])+'/'+str(class_count[i]))

if __name__ == '__main__':
    main()