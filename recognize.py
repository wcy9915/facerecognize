# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 13:29:21 2018

@author: revo1111
"""
import os
import cv2
from read_data import read_name_list
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt

def camera_recognize(path):
    print('Model Loaded.')
    IMAGE_SIZE=128
    fileNum=0
    MODEL_PATH = "D:\\result_module\\train.h5"
    model = load_model(MODEL_PATH)
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        print(sub_path)
        fileNum = fileNum+1 
        print(fileNum)
    #记录学生出勤信息,为0表示旷课，1表示出勤
   
    signed=[]
    #学生数量
    num=fileNum
    print(num)
    i=0
    while i<num:
        signed.append(0)
        i=i+1
    absent_stu=[]
    
    namelist=read_name_list(path)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    face_cascade.load('C:\\Users\\revo1111\\Anaconda3\\envs\\wcy\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml')
    
    cap = cv2.VideoCapture(1)
    if False == cap.isOpened():
        print( 'open video failed')
    else:
        print('open video succeeded')
    cap.set(3, 640) #WIDTH
    cap.set(4, 480) #HEIGHT
    while(True):    
        ret, frame = cap.read()
        if ret==False:
            print("frame is empty")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0: 
            for (x, y, w, h) in faces:
                face= cv2.resize(gray[y:(y + h), x:(x + w)], (200, 200)) 
                face= cv2.resize(face, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_LINEAR)
                img = face.reshape(1, 1, IMAGE_SIZE, IMAGE_SIZE)
                img = img.astype('float32')
                img = img/255.0
                
                result1 = model.predict_proba(img) #测算一下该img属于某个label的概率
                max_index = np.argmax(result1) 
                if result1[0][max_index]>0.8:
                    text=namelist[max_index]
                else:
                    text="stranger"
                
                signed[max_index]=1
                
                cv2.putText(frame, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)  #显示名字
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  #在人脸区域画一个正方形出来
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    count=0
    print("Absent classmate:")
    while count<num:
        if signed[count]==0:
            absent_stu.append(namelist[count])
            print(namelist[count])
        count=count+1
    
    return absent_stu  

if __name__ == '__main__':
    camera = camera_recognize('D:\\result_info')
