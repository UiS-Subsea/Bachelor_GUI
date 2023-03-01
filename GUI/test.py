from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton
import sys
import datetime
import time


class MyWindow(QMainWindow):
    def __init__(self):#Everything that goes in the window goes into this function
        super(MyWindow, self).__init__() #Think about self as the window 
        uic.loadUi("temperatur.ui", self)
        self.counter=0
        self.timer=QtCore.QTimer()
        self.timer.setInterval(1000)
        self.connectFunctions()
        self.timer.start()
        
    
    def connectFunctions(self):    
        self.timer.timeout.connect(self.update_label)
        self.dangerButton.clicked.connect(self.oh_no)
        
    
    #def buttonClick(self):
    #    self.label1.setText("You pressed the button")
        
    def update_label(self):
        self.counter+=1
        self.tempLabel.setText(str(self.counter))
    
    def oh_no(self):
    
        time.sleep(5)
        print("oh no")
        

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()