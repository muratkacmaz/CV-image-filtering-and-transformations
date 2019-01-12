#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 00:31:41 2018

@author: muratkacmaz
"""

#Murat Kaçmaz 150140052

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout,QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np 
import statistics
import cv2

##########################################
## Do not forget to delete "return NotImplementedError"
## while implementing a function
########################################

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.showFullScreen()
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.title = 'Filtering & Geometric Transforms' 
        self.setWindowTitle(self.title)
        self.initUI()


    
    def openImage(self):
        self.imageLabel = QLabel('image')
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
       
 
        self.image = cv2.imread(imagePath)
        self.image  = cv2.cvtColor(self.image , cv2.COLOR_BGR2RGB)
        
        
        self.imageRed= self.image [:,:,0]
        row,column= self.imageRed.shape 
        bytesPerLine = 3 * column
        self.saveImage = np.zeros((row,column,3),dtype= np.uint8)
        imagePixmap = QImage(self.image.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.imageLabel.setPixmap(QPixmap.fromImage(imagePixmap))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageBox.layout().addWidget(self.imageLabel)
        

    
    def saveImage(self):
        self.saveImage  = cv2.cvtColor(self.saveImage , cv2.COLOR_RGB2BGR)
        name =QFileDialog.getSaveFileName(self,'Save',"Saved")
        cv2.imwrite("150140052.png", self.saveImage)
        
        
    
    def closeApp(self):
        app.quit()
        return NotImplementedError
  
    
    def averageFilters(self,value):
        half =int(value/2)
        summ = np.zeros(3)
        sq = value*value
        self.newImageAv = self.image
      
        row,column= self.imageRed.shape 
        bytesPerLine = 3*column
        for r in range(row):
            for c in range(column):
                for i in range(value):
                    for j in range(value):
                        if(r-half+i < 0 or r+half+i >row or c-half+j<0 or c+half+j>column):
                            continue
                        summ += self.image[r-half+i][c-half+j]  
                self.newImageAv[r][c] = summ/sq 
                summ = np.zeros(3)
                
        imagePixmap = QImage(self.newImageAv.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.imageLabel.setPixmap(QPixmap.fromImage(imagePixmap))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageBox.layout().addWidget(self.imageLabel)
        self.saveImage = self.newImageAv
        
        
    def gaussianFilters(self,value): #change it 
        half =int(value/2)
        summ = np.zeros(3)
        sq = value*value
        self.newImageGa = self.image
      
        row,column= self.imageRed.shape 
        bytesPerLine = 3*column
        for r in range(row):
            for c in range(column):
                for i in range(value):
                    for j in range(value):
                        if(r-half+i < 0 or r+half+1+i >=row or c-half+j<0 or c+half+1+j>=column):
                            continue
                        summ += self.image[r-half+i][c-half+j]  #
                self.newImageGa[r][c] = summ/sq 
                summ = np.zeros(3)
          
                
        imagePixmap = QImage(self.newImageGa.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.imageLabel.setPixmap(QPixmap.fromImage(imagePixmap))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageBox.layout().addWidget(self.imageLabel)
        self.saveImage = self.newImageGa
    
        
    def medianFilters(self,value):
        half =int(value/2)
        sq = value*value
        self.newImageMed = self.image
        medianRed= np.zeros(sq)
        medianGreen = np.zeros(sq)
        medianBlue= np.zeros(sq)
        row,column= self.imageRed.shape 
        bytesPerLine = 3*column
        squareTraveler = 0 
        for r in range(row):
            for c in range(column):
                for i in range(value):
                    for j in range(value):
                        if(r-half+i < 0 or r+half+1+i >=row or c-half+j<0 or c+half+1+j>=column):
                            medianRed[squareTraveler] = 0
                            medianGreen[squareTraveler] = 0
                            medianBlue[squareTraveler] = 0
                            squareTraveler = squareTraveler+1
                            continue 
                        medianRed[squareTraveler] = self.image[r-half+i][c-half+j][0]  
                        medianGreen[squareTraveler] = self.image[r-half+i][c-half+j][1]
                        medianBlue[squareTraveler] = self.image[r-half+i][c-half+j][2]
                        squareTraveler = squareTraveler+1
                squareTraveler = 0
                self.newImageMed[r][c][0] = statistics.median(medianRed)
                self.newImageMed[r][c][1] = statistics.median(medianGreen)
                self.newImageMed[r][c][2] = statistics.median(medianBlue)
                medianRed= np.zeros(value*value)
                medianGreen = np.zeros(value*value)
                medianBlue= np.zeros(value*value)
               
        imagePixmap = QImage(self.newImageMed.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.imageLabel.setPixmap(QPixmap.fromImage(imagePixmap))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageBox.layout().addWidget(self.imageLabel)
        self.saveImage = self.newImageMed
        
       
        
    def rotate(self,value):
        if value == 1 :
            print("right")
        elif value == 2 :
            print("left")
        

    def scale(self,value):
        
        row,column= self.imageRed.shape 
        bytesPerLine = 3*column
        r2 =int(row*value)
        c2 =int(column*value)
        self.scaledImage = np.zeros((r2,c2), dtype =np.uint8)
        for r in range(r2):
            for c in range(c2):
                self.scaledImage[r][c] = self.image[int(r/value)][int(c/value)] 
                    

            
        imagePixmap = QImage(self.scaledImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.imageLabel.setPixmap(QPixmap.fromImage(imagePixmap))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageBox.layout().addWidget(self.imageLabel)
        self.saveImage = self.scaledImage
        
    def translate(self,value):
        if value == 1 :
            row,column= self.imageRed.shape 
            bytesPerLine = 3*column
            self.translatedImage = np.zeros((column,row,3), dtype =np.uint8)
            for r in range(row):
                for c in range(column):
                    self.translatedImage[c][row-r-1] = self.image[r][c]
        
            imagePixmap = QImage(self.translatedImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
            self.imageLabel.setPixmap(QPixmap.fromImage(imagePixmap))
            self.imageLabel.setAlignment(Qt.AlignCenter)
            self.imageBox.layout().addWidget(self.imageLabel)
            self.saveImage = self.translatedImage
        elif value == 2 :
            row,column= self.imageRed.shape 
            bytesPerLine = 3*column
            self.translatedImage = np.zeros((column,row,3), dtype =np.uint8)
            
            for r in range(row):
                for c in range(column):
                    self.translatedImage[column-c-1][r] = self.image[r][c]
        
            imagePixmap = QImage(self.translatedImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
            self.imageLabel.setPixmap(QPixmap.fromImage(imagePixmap))
            self.imageLabel.setAlignment(Qt.AlignCenter)
            self.imageBox.layout().addWidget(self.imageLabel)
            self.saveImage = self.translatedImage
    
    def initUI(self):
        self.gLayout = QGridLayout()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        filtersMenu = mainMenu.addMenu("&Filters")
        geoMenu = mainMenu.addMenu("&Geometric Transforms")
        
        
        openn = QAction ("&Open",self)
        openn.triggered.connect(self.openImage)
        save = QAction ("&Save",self)
        save.triggered.connect(self.saveImage)
        exxit = QAction ("&EX1IT",self)
        exxit.triggered.connect(self.closeApp)
        fileMenu.addAction(openn)
        fileMenu.addAction(save)
        fileMenu.addAction(exxit)
        
        average_menu= filtersMenu.addMenu('Average Filters')
        threeXthree = QAction ("&3x3",self)
        threeXthree.triggered.connect(lambda:self.averageFilters(3))
        fiveXfive = QAction ("&5x5",self)
        fiveXfive.triggered.connect(lambda:self.averageFilters(5))
        sevenXseven = QAction ("&7x7",self)
        sevenXseven.triggered.connect(lambda:self.averageFilters(7))
        nineXnine = QAction ("&9x9",self)
        nineXnine.triggered.connect(lambda:self.averageFilters(9))
        eleXele = QAction ("&11x11",self)
        eleXele.triggered.connect(lambda:self.averageFilters(11))
        thirtXthirt = QAction ("&13x13",self)
        thirtXthirt.triggered.connect(lambda:self.averageFilters(13))
        fiftXfift = QAction ("&15x15",self)
        fiftXfift.triggered.connect(lambda:self.averageFilters(15))
        average_menu.addAction(threeXthree)
        average_menu.addAction(fiveXfive)
        average_menu.addAction(sevenXseven)
        average_menu.addAction(nineXnine)
        average_menu.addAction(eleXele)
        average_menu.addAction(thirtXthirt)
        average_menu.addAction(fiftXfift)
        
        gaussian_menu= filtersMenu.addMenu('Gaussian Filters')
        g_threeXthree = QAction ("&3x3",self)
        g_threeXthree.triggered.connect(lambda:self.gaussianFilters(3))
        g_fiveXfive = QAction ("&5x5",self)
        g_fiveXfive.triggered.connect(lambda:self.gaussianFilters(5))
        g_sevenXseven = QAction ("&7x7",self)
        g_sevenXseven.triggered.connect(lambda:self.gaussianFilters(7))
        g_nineXnine = QAction ("&9x9",self)
        g_nineXnine.triggered.connect(lambda:self.gaussianFilters(9))
        g_eleXele = QAction ("&11x11",self)
        g_eleXele.triggered.connect(lambda:self.gaussianFilters(11))
        g_thirtXthirt = QAction ("&13x13",self)
        g_thirtXthirt.triggered.connect(lambda:self.gaussianFilters(13))
        g_fiftXfift = QAction ("&15x15",self)
        g_fiftXfift.triggered.connect(lambda:self.gaussianFilters(15))
        gaussian_menu.addAction(g_threeXthree)
        gaussian_menu.addAction(g_fiveXfive)
        gaussian_menu.addAction(g_sevenXseven)
        gaussian_menu.addAction(g_nineXnine)
        gaussian_menu.addAction(g_eleXele)
        gaussian_menu.addAction(g_thirtXthirt)
        gaussian_menu.addAction(g_fiftXfift)
        

        median_menu= filtersMenu.addMenu('Median Filters')
        m_threeXthree = QAction ("&3x3",self)
        m_threeXthree.triggered.connect(lambda:self.medianFilters(3))
        m_fiveXfive = QAction ("&5x5",self)
        m_fiveXfive.triggered.connect(lambda:self.medianFilters(5))
        m_sevenXseven = QAction ("&7x7",self)
        m_sevenXseven.triggered.connect(lambda:self.medianFilters(7))
        m_nineXnine = QAction ("&9x9",self)
        m_nineXnine.triggered.connect(lambda:self.medianFilters(9))
        m_eleXele = QAction ("&11x11",self)
        m_eleXele.triggered.connect(lambda:self.medianFilters(11))
        m_thirtXthirt = QAction ("&13x13",self)
        m_thirtXthirt.triggered.connect(lambda:self.medianFilters(13))
        m_fiftXfift = QAction ("&15x15",self)
        m_fiftXfift.triggered.connect(lambda:self.medianFilters(15))
        median_menu.addAction(m_threeXthree)
        median_menu.addAction(m_fiveXfive)
        median_menu.addAction(m_sevenXseven)
        median_menu.addAction(m_nineXnine)
        median_menu.addAction(m_eleXele)
        median_menu.addAction(m_thirtXthirt)
        median_menu.addAction(m_fiftXfift)

        rotate_menu= geoMenu.addMenu('Rotate')
        r_right = QAction ("&Rotate 10 Degree Right",self)
        r_right.triggered.connect(lambda:self.rotate(1))
        r_left = QAction ("&Rotate 10 Degree Left",self)
        r_left.triggered.connect(lambda:self.rotate(2))
        rotate_menu.addAction(r_right)
        rotate_menu.addAction(r_left)
        
        scale_menu= geoMenu.addMenu('Scale')
        scale2x = QAction ("&2x",self)
        scale2x.triggered.connect(lambda:self.scale(2))
        scale12x = QAction ("&1/2x",self)
        scale12x.triggered.connect(lambda:self.scale(0.5))
        scale_menu.addAction(scale2x)
        scale_menu.addAction(scale12x)
        
        translate_menu= geoMenu.addMenu('Translate')
        t_right = QAction ("&Right",self)
        t_right.triggered.connect(lambda:self.translate(1))
        t_left = QAction ("&Left",self)
        t_left.triggered.connect(lambda:self.translate(2))
        translate_menu.addAction(t_right)
        translate_menu.addAction(t_left)

        self.imageBox = QGroupBox()
        imageLayout = QVBoxLayout()
        self.imageBox.setLayout(imageLayout)
        
      
        self.gLayout.addWidget(self.imageBox)
       
        self.window.setLayout(self.gLayout)
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())