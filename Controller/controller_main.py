import json
import multiprocessing
import threading
import time
from Threadwatch import Threadwatcher
import Controller_Handler as controller

# VALUES: (0-7) -> index i: [0,0,0,0,0,0,0,0]
#MANIPULATOR
MANIPULATOR_IN_OUT = 0
MANIPULATOR_ROTATION = 1
MANIPULATOR_TILT = 2
MANIPULATOR_GRAB_RELEASE = 3

#ROV
X_AXIS = 1
Y_AXIS = 0
Z_AXIS = 6
ROTATION_AXIS = 2

class Rov_state:
    def __init__(self, queue, t_watch: Threadwatcher) -> None:
        self.t_watch: Threadwatcher = t_watch
        self.data:dict = {}
        self.packets_to_send = []
        self.queue: multiprocessing.Queue = queue


    def build_manipulator_packet(self):
        data = [0,0,0,0,0,0,0,0]
        data[0] = self.data["mani_joysticks"][MANIPULATOR_IN_OUT]
        data[1] = self.data["mani_joysticks"][MANIPULATOR_ROTATION]
        data[2] = self.data["mani_joysticks"][MANIPULATOR_TILT]
        data[3] = self.data["mani_joysticks"][MANIPULATOR_GRAB_RELEASE]
        self.packets_to_send.append([41, data])

    #KAN OGSÅ GJØRES SLIK VED Å LEGGE TIL I LISTEN:
    def build_rov_packet(self):
        data = [0,0,0,0,0,0,0,0]
        data[0] = self.data["rov_joysticks"][X_AXIS]
        data[1] = self.data["rov_joysticks"][Y_AXIS]
        data[2] = self.data["rov_joysticks"][Z_AXIS]
        data[3] = self.data["rov_joysticks"][ROTATION_AXIS]
        self.packets_to_send.append([40, data])


    def craft_packet(self, t_watch: Threadwatcher, id):
        while t_watch.should_run(id):
            userinput = input("Packet: [parameter_id of type int, value of type float or int]: ")
            var = []
            try:
                var = json.loads(userinput)
                if not isinstance(var[0], int):
                    print("Error: parameter id was not an int! try again.")
                    continue
                # if not isinstance(var[1], int) or not isinstance(var[1], float):
                #     print("Error: parameter id was not an int or float! try again.")
                #     continue
                if len(var) != 2:
                    print("Error: list was not length 2")
                    continue
            except Exception as e:
                print(f"Error when parsing input\n {e}")
                continue

            self.packets_to_send.append([201, var])

    def get_from_queue(self):
        """Takes data from the queue and sends it to the correct handler"""
        id = -1
        packet = ""
        try:
            id, packet = self.queue.get()
        except Exception as e:
            # print(f"Error when trying to get from queue. \n{e}")
            return
        if id == 1: # controller data update
            self.data = packet
    
    def check_controls(self):
        self.build_rov_packet()
        self.build_manipulator_packet()

def run(t_watch: Threadwatcher, id: int, queue_for_rov: multiprocessing.Queue):
    rov_state = Rov_state(queue_for_rov, t_watch)
    if run_craft_packet:
        id = t_watch.add_thread()
        threading.Thread(target=rov_state.craft_packet, args=(t_watch, id), daemon=True).start()

    while t_watch.should_run(id):
        rov_state.get_from_queue()
        if run_get_controllerdata and rov_state.data != {}:
            rov_state.check_controls()
        rov_state.data = {}



if __name__ == "__main__":

    try:
        global time_since_start
        global start_time_sec
        global run_gui
        global manual_input_rotation
        global run_network
        global run_craft_packet
        start_time_sec = time.time()
        run_get_controllerdata = True
        run_craft_packet = True
        
        queue_for_rov = multiprocessing.Queue()
        t_watch = Threadwatcher()

        if run_get_controllerdata:
                id = t_watch.add_thread()
                # takes in controller data and sends it into child_conn
                controller_process = multiprocessing.Process(target=controller.run, args=(queue_for_rov, t_watch, id,True, True,), daemon=True)
                controller_process.start()
        
        print("starting send to rov")
        id = t_watch.add_thread()
        main_driver_loop = threading.Thread(target=run, args=(t_watch, id, queue_for_rov), daemon=True)
        main_driver_loop.start()
        
    except KeyboardInterrupt:
            t_watch.stop_all_threads()
            print("stopped all threads")