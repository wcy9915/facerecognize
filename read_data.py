# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 13:36:26 2018

@author: revo1111
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from read_img import endwith

#输入一个文件路径，对其下的每个文件夹下的图片读取，并对每个文件夹给一个不同的Label
#返回一个img的list,返回一个对应label的list,返回一下有几个文件夹（有几种label)

def read_file(path):
    img_list = []
    label_list = []
    dir_counter = 0
    IMG_SIZE = 128

    #对路径下的所有子文件夹中的所有jpg文件进行读取并存入到一个list中
    for child_dir in os.listdir(path):
         child_path = os.path.join(path, child_dir)
         print(child_dir)
         for dir_image in  os.listdir(child_path):
             if endwith(dir_image,'jpg'):
                print(dir_image)
                img = cv2.imread(os.path.join(child_path, dir_image))
                resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                recolored_img = cv2.cvtColor(resized_img,cv2.COLOR_BGR2GRAY)
                img_list.append(recolored_img)
                label_list.append(dir_counter)

         dir_counter += 1

    # 返回的img_list转成了 np.array的格式
    #Pyhton list需要n个指针，和n个对象
    #np.array储存单一数据类型的多维数组
    img_list = np.array(img_list)

    return img_list,label_list,dir_counter

#读取训练数据集的文件夹，把他们的名字返回给一个list
def read_name_list(path):
    name_list = []
    for child_dir in os.listdir(path):
        name_list.append(child_dir)
        
    print(name_list)
    return name_list



if __name__ == '__main__':
    img_list,label_lsit,counter = read_file('D:\\result_face3')
    print(counter)

