# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 17:27:18 2018

@author: revo1111
"""

from PyQt5 import QtWidgets
from signed_up import Ui_Dialog as U1
from import_pic import Ui_Dialog as U2
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import *
from pick_face import readPicSaveFace
from recognize import camera_recognize
from train import train_
import pandas as pd
import os
import sys

class mywindow(QtWidgets.QWidget, U1):
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.write_img)
        self.pushButton_4.clicked.connect(self.Button_4_clicked) 
        self.pushButton_2.clicked.connect(self.Button_2_clicked)
        self.path='D:\\result_info'
        self.file_path=''
        self.absent_stu=[]
        
    def write_img(self):
        #选取文件夹
        self.file_path = self.lineEdit.text()
        if self.file_path and os.path.exists(self.file_path):           
            self.ui = w2() 
            self.ui.getpath(self.file_path)
            self.ui.show() 
            self.ui.exec_()
        else:
            print('failed')
            
    def Button_4_clicked(self):
        self.file_path = self.lineEdit.text()
        if not os.path.exists(self.path):    
            os.mkdir(self.path)
        readPicSaveFace(self.file_path,self.path,'.jpg','.JPG','png','PNG')
        train_(self.path)
        return
    
    def Button_2_clicked(self):        
        self.absent_stu=camera_recognize(self.path)
        count=0
        self.ui = MyDialog()
        self.ui.getinfo(self.absent_stu)
        self.ui.show() 
        self.ui.exec_()
            
            
class w2(QtWidgets.QDialog,U2):
    def  __init__ (self):
        super(w2, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.path=''
        
    def getpath(self,file_path):
        self.path=file_path        
       
    def pushButton_clicked(self):
        stu_num=self.lineEdit.text()
        os.mkdir(os.path.join(self.path,stu_num))
        path=str(os.path.join(self.path,stu_num))
        try:
            os.startfile(str(path))
        except:
            print('failed')          

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.MyTable = QTableWidget(50,2)
        self.MyTable.setHorizontalHeaderLabels(['学号'])
        self.stu_info=""
        
    def getinfo(self,absent_stu):
        self.stu_info=absent_stu
        count=0
        for i in self.stu_info:           
            newItem = QTableWidgetItem(i)
            self.MyTable.setItem(count,0, newItem)
            count=count+1
        
        
      
        layout = QHBoxLayout()
        layout.addWidget(self.MyTable)
        self.setLayout(layout)          
                 
    
if __name__ == '__main__':

    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()    
    ui.show()
    sys.exit(app.exec_())
