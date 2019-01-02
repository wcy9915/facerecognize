# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 09:17:44 2018

@author: revo1111
"""

from keras.layers import Conv2D
from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten,MaxPooling2D,Dropout
from sklearn.model_selection import  train_test_split
from read_data import read_file
from keras.utils import np_utils
import random
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD



def train_(path):
    module_path="D:\\result_module"
    if not os.path.exists(module_path):
        os.mkdir(module_path)
    FILE_PATH = "D:\\result_module\\train.h5"
    IMAGE_SIZE=128
    print(path)
    imgs,labels,counter = read_file(path)

    #X为对应的样本集，Y为对应的标签集
    #训练集：测试集=8：2
    X_train,X_test,y_train,y_test = train_test_split(imgs,labels,test_size=0.2,random_state=random.randint(0, 100))
    X_train = X_train.reshape(X_train.shape[0], 1,IMAGE_SIZE, IMAGE_SIZE)
    X_test = X_test.reshape(X_test.shape[0], 1,IMAGE_SIZE, IMAGE_SIZE) 
    #数据归一化
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32') 
    X_train=X_train/255.0
    X_test=X_test/255.0
    
    Y_train = np_utils.to_categorical(y_train, counter)
    Y_test = np_utils.to_categorical(y_test, counter)
    #构建卷积神经网络
    face_recognition_model = Sequential() 
    #32个卷积核，每个卷积核5*5，padding='same'表示在不够卷积核大小时，进行填充
    face_recognition_model.add(Conv2D(filters=32,
                                kernel_size=(3, 3),
                                padding='same',
                                dim_ordering='th',
                                input_shape=X_train.shape[1:]))
    face_recognition_model.add(Activation('relu'))
    
    #face_recognition_model.add(Conv2D(filters=32,
    #                            kernel_size=(3, 3)))
    #face_recognition_model.add(Activation('relu'))
    #指定池化窗口的大小，以及池化操作的移动步幅
    face_recognition_model.add(MaxPooling2D(pool_size=(2, 2),
                                            strides=(2, 2),
                                            padding='same'))
    face_recognition_model.add(Dropout(0.25))

    face_recognition_model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='same'))
    face_recognition_model.add(Activation('relu'))
    #face_recognition_model.add(Conv2D(filters=64,
    #                            kernel_size=(3, 3)))
    #face_recognition_model.add(Activation('relu'))
    
    
    face_recognition_model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    face_recognition_model.add(Dropout(0.25))
    
    face_recognition_model.add(Flatten())
    face_recognition_model.add(Dense(512))
    face_recognition_model.add(Activation('relu'))
    face_recognition_model.add(Dropout(0.5))

    face_recognition_model.add(Dense(counter))
    face_recognition_model.add(Activation('softmax'))
    face_recognition_model.summary()

    #face_recognition_model.compile(
    #        optimizer='adam',  #有很多可选的optimizer，例如RMSprop,Adagrad，你也可以试试哪个好，我个人感觉差异不大
    #        loss='categorical_crossentropy',  #你可以选用squared_hinge作为loss看看哪个好
    #        metrics=['accuracy'])

    learning_rate=0.01
    decay=1e-6
    momentum=0.9
    nesterov=True
    sgd=SGD(lr=learning_rate,decay=decay,momentum=momentum, nesterov=nesterov)
    face_recognition_model.compile(loss='categorical_crossentropy',
                             optimizer=sgd,
                             metrics=['accuracy'])
    #datagen = ImageDataGenerator(featurewise_center = False,samplewise_center  = False,             #是否使输入数据的每个样本均值为0
    #            featurewise_std_normalization = False,  #是否数据标准化（输入数据除以数据集的标准差）
    #            samplewise_std_normalization  = False,  #是否将每个样本数据除以自身的标准差
    #            zca_whitening = False,                  #是否对输入数据施以ZCA白化
    #            rotation_range = 20,                    #数据提升时图片随机转动的角度(范围为0～180)
    #            width_shift_range  = 0.2,               #数据提升时图片水平偏移的幅度（单位为图片宽度的占比，0~1之间的浮点数）
    #            height_shift_range = 0.2,               #同上，只不过这里是垂直
    #            horizontal_flip = True,                 #是否进行随机水平翻转
    #            vertical_flip = False)  
    face_recognition_model.fit(X_train,
                            Y_train,
                            batch_size =20,
                            epochs =11,
                            validation_data = (X_test, Y_test),
                            shuffle=True)
    #datagen.fit(X_train)       
    #face_recognition_model.fit_generator(datagen.flow(X_train, Y_train,batch_size = 20),
    #                                   samples_per_epoch = X_train.shape[0],nb_epoch =30,
    #                                     validation_data=(X_test, Y_test))

    print('\nTesting---------------')
    loss, accuracy =face_recognition_model.evaluate(X_test,Y_test)


    print('test loss;', loss)
    print('test accuracy:', accuracy)


    print('Model Saved.')
    face_recognition_model.save(FILE_PATH)

if __name__ == '__main__':
    train_('D:\\Face_recognize\\result_face2')