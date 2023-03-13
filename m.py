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
    thrust_list = [num for num in range(-100,101)]
    power_list = [num for num in range(0, 101)]
    count = -1
    sensordata = {}
    while True:
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
