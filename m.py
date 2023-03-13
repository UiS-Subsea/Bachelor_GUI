import time
from multiprocessing import Process, Pipe
from GUI import gui_loop_test
import threading
import multiprocessing
import atexit

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



class ROV_test:
    def __init__(self, gui_pipe):
        self.gui_pipe = gui_pipe
        self.sensordata = None
        self.start_time = time.time()
        self.time_since_packet_update = []
        self.send_sensordata_to_gui(self.sensordata)
        self.main_loop()
        

    def send_sensordata_to_gui(self, data):
            print(f"sending data from main to gui: {data =}")
            self.gui_pipe.send(data)

def send_fake_sensordata(gui_pipe: multiprocessing.Pipe):

if __name__ == "__main__":
    global start_time_sec
    global time_since_start
    global run_gui
    run_send_fake_sensordata=True 
    run_gui = True
    gui_parent_pipe, gui_child_pipe = Pipe()
    start_time_sec = time.time()
    def stop_datafaker():
        datafaker.join()
    if run_gui:
        gui_loop = Process(target=gui_loop_test.window, args=(gui_child_pipe,), daemon=True)
        gui_loop.start()
        
    if run_send_fake_sensordata:
        datafaker = threading.Thread(target=send_fake_sensordata, args=(gui_parent_pipe,), daemon=True)
        atexit.register(stop_datafaker)
        datafaker.start()
