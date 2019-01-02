# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:51:13 2018

@author: revo1111
"""

import os
import cv2


#根据输入的文件夹绝对路径，将该文件夹下的所有指定suffix的文件读取存入一个list,该list的第一个元素是该文件夹的名字
def readAllImg(path,*suffix):
    try:
        #os.listdir返回一个由文件名和目录名组成的列表，此处为path下所有的文件和目录名称
        s = os.listdir(path)
        resultArray = []
        #os.path.basename返回最后的文件名
        fileName = os.path.basename(path)
        resultArray.append(fileName)

        for i in s:
            #筛选出图片文件
            if endwith(i, suffix):
                #将path和i组合之后返回
                document = os.path.join(path, i)
                img = cv2.imread(document)
                try:
                    img.shape 
                except:
                    print('fail to read xxx.jpg')

                resultArray.append(img)


    except IOError:
        print ("Error")

    else:
        print ("读取成功")
        return resultArray

#输入一个字符串一个标签，对这个字符串的后续和标签进行匹配
def endwith(s,*endstring):
    #Map函数接受一个函数和一个list，并通过吧函数f依次作用在list的每个元素上，得到并返回一个新的list
   resultArray = map(s.endswith,endstring)
   if True in resultArray:
       return True
   else:
       return False

if __name__ == '__main__':

  result = readAllImg("D:\\face_result_test",'.pgm')
  print (result[0])
  # cv2.namedWindow("Image")
  # cv2.imshow("Image", result[1])
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()