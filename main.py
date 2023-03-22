# is empty
# testing for saving to windows kappa xd xd

import json
import multiprocessing
from Kommunikasjon.network_handler import Network
from multiprocessing import Process, Pipe
import threading
import time
from Thread_info import Threadwatcher
from Controller import Controller_Handler as controller
import gui
from gui import guiFunctions as f

# VALUES: (0-7) -> index i: [0,0,0,0,0,0,0,0]
# MANIPULATOR
MANIPULATOR_IN_OUT = 0
MANIPULATOR_ROTATION = 1
MANIPULATOR_TILT = 2
MANIPULATOR_GRAB_RELEASE = 3

# ROV
X_AXIS = 1
Y_AXIS = 0
Z_AXIS = 6
ROTATION_AXIS = 2


def network_format(data) -> bytes:
    """Formats the data for sending to network handler"""
    packet_seperator = json.dumps("*")
    return bytes(packet_seperator+json.dumps(data)+packet_seperator, "utf-8")


class Rov_state:
    def __init__(self, queue,gui_pipe, t_watch: Threadwatcher) -> None:
        self.t_watch: Threadwatcher = t_watch
        self.data: dict = {}
        self.logger = Logger()
        self.queue: multiprocessing.Queue = queue
        self.gui_pipe = gui_pipe # Pipe to send sensordata back to the gui
        self.sensordata=None
        self.send_sensordata_to_gui()
        
        # Pipe to send sensordata back to the gui
        # Prevents the tilt toggle from toggling back again immediately if we hold the button down
        self.camera_toggle_wait_counter: int = 0
        # Tilt in degrees of the camera servo motors.
        self.camera_tilt: float[list] = [0, 0]
        # Turn the ability to change camera tilt, when camera processing is happening on the camera.
        self.camera_tilt_allowed = [True, True]  # [cam 0, cam 1]
        # Toggles between controlling rotation or camera tilt on right joystick
        self.camera_tilt_control_false = False
        # Network handler that sends data to rov (and recieves)
        self.network_handler: Network = network_handler

        self.camera_is_on = [True, True]
        self.camera_command: list[list[int, dict]] = None
        self.regulator_active: list[bool] = [True, True, True]
        self.joystick_moves_camera = False
        self.camera_mode = [0, 1, 2, 3, 4, 5]
        self.active_camera = 0
        self_hud_camera_status = False

        self.packets_to_send = []
    
    def send_sensordata_to_gui(self,data):
        """Sends sensordata to the gui"""
        if self.sensordata == None:
            return
        self.gui_pipe.send(data)

    def build_rov_packet(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]
        data[0] = self.data["rov_joysticks"][X_AXIS]
        data[1] = self.data["rov_joysticks"][Y_AXIS]
        data[2] = self.data["rov_joysticks"][Z_AXIS]
        data[3] = self.data["rov_joysticks"][ROTATION_AXIS]
        self.packets_to_send.append([40, data])
        # print(self.packets_to_send)

    def build_manipulator_packet(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]
        data[0] = self.data["mani_joysticks"][MANIPULATOR_IN_OUT]
        data[1] = self.data["mani_joysticks"][MANIPULATOR_ROTATION]
        data[2] = self.data["mani_joysticks"][MANIPULATOR_TILT]
        data[3] = self.data["mani_joysticks"][MANIPULATOR_GRAB_RELEASE]
        self.packets_to_send.append([41, data])
        # print(self.packets_to_send)

    def button_handling(self):
        rov_buttons = self.data.get("rov_buttons")
        mani_buttons = self.data.get("mani_buttons")
        # print(f"KNAPPER {rov_buttons} : {mani_buttons}")

    def get_from_queue(self):
        """Takes data from the queue and sends it to the correct handler"""
        id = -1
        packet = ""
        try:
            id, packet = self.queue.get()
        except Exception as e:
            # print(f"Error when trying to get from queue. \n{e}")
            return
        if id == 1:  # controller data update
            self.data = packet

    def check_controls(self):
        # self.button_handling()
        self.build_rov_packet()
        self.build_manipulator_packet()


def run(network_handler: Network, t_watch: Threadwatcher, id: int, queue_for_rov: multiprocessing.Queue):
    rov_state = Rov_state(queue_for_rov, t_watch)

    # Con. del
    while t_watch.should_run(id):
        rov_state.get_from_queue()
        if run_get_controllerdata and rov_state.data != {}:
            rov_state.check_controls()
        rov_state.data = {}

    # Komm. del
    print("run thread")
    print(f"{network_handler = }")
    rov_state = Rov_state(queue_for_rov, network_handler, gui_pipe, t_watch)
    print(f"{network_handler = }")
    if not network_handler == None:
        id = t_watch.add_thread()
        threading.Thread(target=rov_state.recieve_data_from_rov, args=(
            network_handler, t_watch, id), daemon=True).start()
    if run_craft_pakcet:
        id = t_watch.add_thread()
        threading.Thread(target=rov_state.craft_packet,
                         args=(t_watch, id), daemon=True).start()
    while t_watch.should_run(id):
        rov_state.send_packets()
        rov_state.data = {}


if __name__ == "__main__":

    try:
        global run_gui
        global run_network
        global network
        global run_craft_packet
        run_craft_pakcet = True
        run_network = True #Bytt t false når du ska prøva å connecte.
        run_gui = True
        run_get_controllerdata = True
        run_send_fake_sensordata=True #Sett til True om du vil sende fake sensordata til gui
        
        
        queue_for_rov = multiprocessing.Queue()
        
        (
            gui_parent_pipe,#Used by main process, to send/receive data to gui
            gui_child_pipe,#Used by gui process, to send/receive data to main
        ) = Pipe()  # starts the gui program. gui_parent_pipe should get the sensor data
        
        t_watch = Threadwatcher()
        debug_all = False #Sett til True om du vil se input fra controllers

        network = False
        if not run_network:
            network = Network(is_server=False, port=6900, bind_addr="0.0.0.0",
                              connect_addr="10.0.0.2")
            print("network started")
            run_network = True

        print("starting send to rov")
        id = t_watch.add_thread()
        print(id)
        main_driver_loop = threading.Thread(target=run, args=(
            network, t_watch, id, queue_for_rov), daemon=True)
        main_driver_loop.start()
    # alt oppe er komm. del

        if run_get_controllerdata:
            id = t_watch.add_thread()
            # takes in controller data and sends it into child_conn
            controller_process = Process(target=controller.run, args=(queue_for_rov, t_watch, id, True, debug_all), daemon=True)
            controller_process.start()
            input("Press Enter to start sending!")
            # controller_process.terminate()
        
        if run_gui:
            id = t_watch.add_thread()
            gui_loop = Process(
                target=gui.run,
                args=(gui_child_pipe, queue_for_rov, t_watch, id),
                daemon=True,
            )  # and should recieve commands from the gui
            gui_loop.start()
            print("gui started")

        print("starting send to rov")
        id = t_watch.add_thread()
        main_driver_loop = threading.Thread(
            target=run, args=(t_watch, id, queue_for_rov), daemon=True)
        main_driver_loop.start()
        
        if run_send_fake_sensordata:
            id = t_watch.add_thread()
            datafaker = threading.Thread(
                target=f.send_fake_sensordata(),
                args=(t_watch, gui_parent_pipe),
                daemon=True,
            )
            datafaker.start()

    except KeyboardInterrupt:
            t_watch.stop_all_threads()
            print("stopped all threads")




