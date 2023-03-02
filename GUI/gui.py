from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton
import sys


class MyWindow(QMainWindow):
    def __init__(self):#Everything that goes in the window goes into this function
        super(MyWindow, self).__init__() #Think about self as the window 
        uic.loadUi("gui.ui", self)
        self.connectFunctions()
    
    def connectFunctions(self):    
        self.button1.clicked.connect(self.buttonClick)
    
    def buttonClick(self):
        self.label1.setText("You pressed the button")

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()