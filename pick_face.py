# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 14:58:39 2018

@author: revo1111
"""

import os
import cv2
import time
from read_img import readAllImg



#从源路径中读取所有图片，然后逐一进行检查，把其中的脸扣下来，存储到目标路径中
#sourcepath源文件,objectPath目标文件，*suffix为图片类型
def readPicSaveFace(sourcePath,objectPath,*suffix):
    for child_dir in os.listdir(sourcePath):
            child_path = os.path.join(sourcePath, child_dir)
            folder_name=os.path.basename(child_path)
            try:
        #读取照片,返回图片列表
        
                resultArray=readAllImg(child_path,*suffix)

        #对list中图片逐一进行检查,找出其中的人脸并根据源文件夹名写到目标文件夹下

                count = 1
                face_cascade = cv2.CascadeClassifier('C:\\Users\\revo1111\\Anaconda3\\envs\\wcy\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
                face_path=os.path.join(objectPath,folder_name)
                if not os.path.exists(face_path): 
                    os.mkdir(os.path.join(objectPath,folder_name))
                for i in resultArray:
                    if type(i) != str:
                        gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                        for (x, y, w, h) in faces:
                            
                            listStr = [str(int(time.time())), str(count)]  #以时间戳和读取的排序作为文件名称
                            fileName = ''.join(listStr)

                            f = cv2.resize(gray[y:(y + h), x:(x + w)], (200, 200))
                            object_=os.path.join(objectPath,folder_name)
                            cv2.imwrite(object_+os.sep+'%s.jpg' % fileName, f)
                            count += 1


            except IOError:
                print ("Error")

            else:
                print ('Already read '+str(count-1)+' Faces to Destination '+objectPath)

if __name__ == '__main__':
     readPicSaveFace('D:\\Face_recognize\\face\\face','D:\\Face_recognize\\result2','.jpg','.JPG','png','PNG')