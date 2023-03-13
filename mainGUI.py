import time
from multiprocessing import Process, Pipe
from GUI import gui_loop_test
import threading
import multiprocessing
import atexit
from Thread_info import Threadwatcher
from PyQt5 import QtWidgets, uic, QtCore, QtGui, Qt, QtTest
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton
from GUI_test import loop
def create_test_sensordata(delta, old_sensordata=None):
    # test function
    sensordata = {}
    if old_sensordata is None:
        sensordata = {"tid": int(time.time()-start_time_sec), "dybde": -2500.0, "spenning": 48.0, "temp_rov": 26.0}
    else:
        sensordata["tid"] = int(time.time()-start_time_sec)
        sensordata["dybde"] = old_sensordata["dybde"] + 10*delta
        sensordata["spenning"] = old_sensordata["spenning"] + 0.4*delta
        sensordata["temp_rov"] = old_sensordata["temp_rov"] + 0.3*delta
    return sensordata

class ROV_Manipulator:
    def __init__(self,queue,gui_pipe,t_watch: Threadwatcher)-> None:
        self.queue: multiprocessing.Queue=queue
        self.gui_pipe = gui_pipe
        self.t_watch: Threadwatcher = t_watch
        self.sensordata = None
        self.start_time = time.time()
        self.time_since_packet_update = []
        self.send_sensordata_to_gui(self.sensordata)
        self.main_loop()
        
    def send_sensordata_to_gui(self, data):
            print(f"sending data from main to gui: {data =}")
            self.gui_pipe.send(data)

def send_fake_sensordata(t_watch: Threadwatcher, gui_pipe: multiprocessing.Pipe):
    thrust_list = [num for num in range(-100,101)]
    power_list = [num for num in range(0, 101)]
    count = -1
    sensordata = {}
    while t_watch.should_run(0):
        time_since_start = round(time.time()-start_time_sec)
        count += 1
        sensordata["lekk_temp"] = [True, True, True, (25+count)%60, (37+count)%60, (61+count)%60]
        sensordata["thrust"] = [thrust_list[(0+count)%201], thrust_list[(13+count)%201], thrust_list[(25+count)%201], thrust_list[(38+count)%201], thrust_list[(37+count)%201], thrust_list[(50+count)%201], thrust_list[(63+count)%201], thrust_list[(75+count)%201], thrust_list[(88+count)%201], thrust_list[(107+count)%201]]
        sensordata["power_consumption"] = [power_list[count%101]*13, power_list[count%101]*2.4, power_list[count%101]*0.65]
        sensordata["gyro"] = [(time_since_start*2)%60, time_since_start%90, time_since_start%90]
        sensordata["time"] = [time_since_start]
        sensordata["thrust"] = [thrust_list[(0+count)%201], thrust_list[(13+count)%201], thrust_list[(25+count)%201], thrust_list[(38+count)%201], thrust_list[(37+count)%201], thrust_list[(50+count)%201], thrust_list[(63+count)%201], thrust_list[(75+count)%201], thrust_list[(88+count)%201], thrust_list[(107+count)%201]]
        # sensordata["thrust"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        gui_pipe.send(sensordata)
        time.sleep(1)


def run(conn,queue_for_rov,t_watch:Threadwatcher, id):
    app=QtWidgets.QApplication(sys.argv) #Create an instance of QtWidgets.QApplication
    
    mainWindow= ROV_Manipulator(conn,queue_for_rov,t_watch, id) #Create an instance of our class
    mainWindow.setWindowTitle("UiS Subsea") #Set the window title
    
    GLOBAL_STATE= False #Set a global state variable
    mainWindow.show() #Show the form
    sys.exit(app.exec_()) #Execute the app
    

if __name__ == '__main__':
    global time_since_start
    global start_time_sec
    global run_gui
    run_gui=True
    run_send_fake_sensordata = True
    start_time_sec = time.time()
    
    queue_for_rov = multiprocessing.Queue()
    t_watch = Threadwatcher()
    
    gui_parent_pipe, gui_child_pipe = Pipe()        
    
    #Legg til network seinare
    if run_gui:
        id = t_watch.add_thread()
        main_driver_loop = threading.Thread(target=run, args=(t_watch, id, queue_for_rov, gui_parent_pipe), daemon=True)
        main_driver_loop.start()
    
    if run_send_fake_sensordata:
        id = t_watch.add_thread()
        datafaker = threading.Thread(target=send_fake_sensordata, args=(t_watch, id, gui_child_pipe), daemon=True)
        datafaker.start()
        
        