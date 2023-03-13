from PyQt5 import QtWidgets, uic, QtCore, QtGui, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QGridLayout
import sys
import multiprocessing
import threading
import time
from Thread_info import Threadwatcher

class ROV_Manipulator(QMainWindow):
    #Initialize QWidget Window
    
    def __init__(self,pipe_conn_only_rcv, queue: multiprocessing.Queue, t_watch: Threadwatcher, parent=None):
        super(ROV_Manipulator, self).__init__() #super() is used to access methods from a parent or sibling class
        uic.loadUi("GUI\SubseaTest.ui", self) #loads in the .ui file
        
        #Receiving and sending data
        self.queue : multiprocessing.Queue()= queue  # queue to send data to the main process
        self.pipe_conn_only_rcv = pipe_conn_only_rcv # pipe connection to receive data from main process
        self.receive = threading.Thread(target=self.receive_sensordata, daemon=True,args=(self.pipe_conn_only_rcv))     # thread to receive data from main process
        self.receive.start()                # start receiving data from main process
        #Threadwatcher
        self.t_watch: Threadwatcher = t_watch # threadwatcher to control threads 
        self.id = id # id of the thread
        
        self.gir_verdier = [0,0,0,0,0,0,0,0,0,0]
        
        
    
    def self_decide_gui_update(self, sensordata):
        self.sensor_update_function = {
            "thrust" : self.thrust_update,
            "power_consumption" : self.power_consumption_update,
        }
        for key in sensordata.keys():
            if key in self.sensor_update_function:
                self.sensor.update_function[key](sensordata[key])
                print(f"updating {key} with {sensordata[key]}")


    def thrust_update(self, sensordata):
        print(f"thrust update: {sensordata = }")
        for i in range(len(sensordata)):
            if sensordata[i] > 100:
                sensordata[i] = 100
        self.update_round_percent_visualizer(sensordata[0], self.thrust_label_1)
        self.update_round_percent_visualizer(sensordata[1], self.thrust_label_2)
        self.update_round_percent_visualizer(sensordata[2], self.thrust_label_3)
        self.update_round_percent_visualizer(sensordata[3], self.thrust_label_4)
        self.update_round_percent_visualizer(sensordata[4], self.thrust_label_5)
        self.update_round_percent_visualizer(sensordata[5], self.thrust_label_6)
        self.update_round_percent_visualizer(sensordata[6], self.thrust_label_7)
        self.update_round_percent_visualizer(sensordata[7], self.thrust_label_8)


    def update_round_percent_visualizer(self, value, text_label):
        text_label.setText(str(value))
        self.round_percent_visualizer.setValue(value)
        self.round_percent_visualizer.setFormat(str(value) + "%")
    
    def power_consumption_update(self, sensordata):
        pass
    
    def receive_sensordata(self,conn):
        self.communicate=Communicate()
        self.communicate.data_signal.connect(self.decide_gui_update)
        
class Communicate(QtCore.QObject):
    data_signal=QtCore.pyqtSignal(dict) #signal to send data to the main process