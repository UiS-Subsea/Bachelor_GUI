# is empty
# testing for saving to windows kappa xd xd

import json
import multiprocessing
from Kommunikasjon.network_handler import Network
from multiprocessing import Process, Pipe
import threading
import time
from Kommunikasjon.packet_info import Logger
from Thread_info import Threadwatcher
from camerafeed.GUI_Camerafeed_Main import CameraClass
from Controller import Controller_Handler as controller
import gui
from gui import guiFunctions as f
import queue
# VALUES: (0-7) -> index i: [0,0,0,0,0,0,0,0]
# MANIPULATOR
MANIPULATOR_IN_OUT = 15
MANIPULATOR_ROTATION = 0
MANIPULATOR_TILT = 3
MANIPULATOR_GRAB_RELEASE = 6




# ROV
X_AXIS = 1
Y_AXIS = 0
Z_AXIS = 6
ROTATION_AXIS = 2


ID_DIRECTIONCOMMAND_PARAMETERS = 71
ID_DIRECTIONCOMMAND = 70
ID_camera_tilt_upwards = 200
ID_camera_tilt_downwards = 201

def network_format(data) -> bytes:
    packet_seperator = json.dumps("*")
    return bytes(packet_seperator+json.dumps(data)+packet_seperator, "utf-8")

def run_camera_func(t_watch: Threadwatcher, frame_pipe: multiprocessing.Pipe, id: int):
    camera = CameraClass()
    while t_watch.should_run(id):
        # print("Getting frame")
        frame = camera.get_frame()
        frame_pipe.send(frame)
        time.sleep(1)


def send_fake_sensordata(t_watch: Threadwatcher, gui_pipe: multiprocessing.Pipe):
    thrust_list = [num for num in range(-100, 101)]
    power_list = [num for num in range(0, 101)]
    vinkel_list = [num for num in range(-360, 360)]
    dybde_list = [num for num in range(-100, 0)]
    accel_list = [num for num in range(-100, 101)]
    count = -1
    sensordata = {}
    while t_watch.should_run(0):
        # time_since_start = round(time.time()-start_time_sec)
        count += 1
        sensordata["lekk_temp"] = [
            False,
            True,
            True,
            (25 + count) % 60,
            (37 + count) % 60,
            (61 + count) % 60,
        ]
        sensordata["thrust"] = [
            thrust_list[(0 + count) % 201],
            thrust_list[(13 + count) % 201],
            thrust_list[(25 + count) % 201],
            thrust_list[(38 + count) % 201],
            thrust_list[(37 + count) % 201],
            thrust_list[(50 + count) % 201],
            thrust_list[(63 + count) % 201],
            thrust_list[(75 + count) % 201],
            thrust_list[(88 + count) % 201],
            thrust_list[(107 + count) % 201],
        ]
        sensordata["watt"] = [
            power_list[count % 101] * 13,
            power_list[count % 101] * 2.4,
            power_list[count % 101] * 0.65,
        ]
        sensordata["thrust"] = [
            thrust_list[(0 + count) % 201],
            thrust_list[(13 + count) % 201],
            thrust_list[(25 + count) % 201],
            thrust_list[(38 + count) % 201],
            thrust_list[(37 + count) % 201],
            thrust_list[(50 + count) % 201],
            thrust_list[(63 + count) % 201],
            thrust_list[(75 + count) % 201],
            thrust_list[(88 + count) % 201],
            thrust_list[(107 + count) % 201],
        ]
        sensordata["vinkler"] = [
            vinkel_list[(0 + count) % 201],
            vinkel_list[(45 + count) % 201],
            vinkel_list[(90 + count) % 201]
        ]
        sensordata["dybde"]=[
            dybde_list[(0 + count) % 201],
            dybde_list[(45 + count) % 201],
        ]
        sensordata["accel"] = [
            accel_list[(0 + count) % 201],
        ]
        gui_pipe.send(sensordata)
        time.sleep(1)




class Rov_state:
    def __init__(self, queue, network_handler,gui_pipe, t_watch: Threadwatcher) -> None:
        # Threadwatcher
        self.t_watch: Threadwatcher = t_watch

        self.data: dict = {}
        self.logger = Logger()
        
        #Queue and Pipe
        self.queue: multiprocessing.Queue = queue
        self.gui_pipe = gui_pipe # Pipe to send sensordata back to the gui
        self.sensordata=None
        
        
        
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
        self.valid_gui_commands = ["139", "thrust", "accel", "gyro", "time", "manipulator", "power_consumption"]
    
    def update(self):
        pass
    
    
    def send_sensordata_to_gui(self,data):
        #Sends sensordata to the gui
        print("Enter into send_sensordata_to_gui function")
        if self.sensordata == None:
            print(f"Data did not arrive{data}")
        self.gui_pipe.send(data)
        
    def sending_startup_ids(self):
        self.packets_to_send.append(
            [200, {"camera_tilt_upwards": self.camera_tilt[0]}])
        self.packets_to_send.append(
            [201, {"camera_tilt_downwards": self.camera_tilt[1]}])

    def setting_up_canbus_ids(self):
        self.canbus_id = {
            "camera_tilts_up": 200,
            "camera_tilts_down": 201
        }

    def receive_data_from_rov(self, network: Network, t_watch: Threadwatcher, id: int):
        incomplete_packet = ""
        print("recive data thread")
        while t_watch.should_run(id):
            try:
                data = network.receive()
                if data == b"" or data is None:
                    continue
                else:
                    print(data)
                    if data is None:
                       continue
                    decoded, incomplete_packet = Rov_state.decode_packets(
                        data, incomplete_packet)
                if decoded == []:
                    continue
                for message in decoded:
                    print(message)
                    self.handle_data_from_rov(message)

                    #potentially for the future to get information to the GUI : send_to_gui(Rov_state, message)

            except json.JSONDecodeError as e:
                print(f"{data = }, {e = }")
                pass

    #Decodes the tcp packet/s recieved from the rov

    def send_startup_commands(self):
        self.packets_to_send.append(
            [200, {"tilt": self.camera_tilt[0], "on": True}])
        self.packets_to_send.append(
            [201, {"tilt": self.camera_tilt[1], "on": True}])
        self.packets_to_send.append([64,  []])
        self.packets_to_send.append([96,  []])

    def decode_packets(tcp_data: bytes, end_not_complete_packet="") -> list:
        end_not_complete_packet = ""
        try:
            json_strings = end_not_complete_packet + \
                bytes.decode(tcp_data, "utf-8")
            # print(json_strings)
            # pakken er ikke hel. Dette skal aldri skje sÃ¥ pakken burde bli forkasta
            if not json_strings.startswith('"*"'):
                # print(f"Packet did not start with '*' something is wrong. {end_not_complete_packet}")
                return [], ""
            if not json_strings.endswith('"*"'):  # pakken er ikke hel
                end_not_complete_packet = json_strings[json_strings.rfind(
                    "*")-1:]
                # fjerner den ukomplette pakken. til, men ikke med indexen
                json_strings = json_strings[:json_strings.rfind("*")-1]

            json_list = json_strings.split(json.dumps("*"))
        except Exception as e:
            print(f"{tcp_data = } Got error {e}")
            return []
        decoded_items = []

        for item in json_list:

            if item == '' or item == json.dumps("heartbeat"):
                # print(f"{item = }")
                continue

            else:
                # print(f"{item = }")
                try:
                    item = json.loads(item)
                except Exception as e:
                    print(f"{e = }\n {item = }, {tcp_data = }")
                    with open("errors.txt", 'ab') as f:
                        f.write(tcp_data)
                    continue

                    # exit(0)
                decoded_items.append(item)
        return decoded_items, end_not_complete_packet

    def handle_data_from_rov(self, message: dict):
        if run_network:
            self.logger.data_logger.info(message)
            print(f"{message =}")
        message_name = ""
        if not isinstance(message, dict):
            try:
                print(message)
                return
            except Exception as e:
                print(e)
                return
        if "Error" in message or "info" in message:  # den og
            print(message)
            return
        if "Alarm" in message:
            print(message)      # få meldingen inn i GUI'en
        try:
            message_name = list(message.keys())[0]
            print(type(message_name))
        except Exception as e:
            print(e)
            return
        if message_name in self.valid_gui_commands:
            print(f"HERE IS MESSAGE NAME",message_name)
            self.send_sensordata_to_gui(message)
        else:
            pass
            print(f"\n\nMESSAGE NOT RECOGNISED\n{message}\n")

    # def network_format(data) -> bytes:
    #     """Formats the data for sending to network handler"""
    #     packet_seperator = json.dumps("*")
    #     return bytes(packet_seperator+json.dumps(data)+packet_seperator, "utf-8")

    def craft_packet(self, t_watch: Threadwatcher, id):
        print("CraftPack Thread")
        while t_watch.should_run(id):
            print("HELLO!")
            userinput = input(
                "Packet: [parameter_id of type int, value of type float or int]: ")
            var = []
            try:
                print("TRY")
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
            print(var)
            #self.packets_to_send.append([ID_DIRECTIONCOMMAND_PARAMETERS, var])
            self.packets_to_send.append([var[0], var[1]])

    def send_packets(self):
        """Sends the created network packets and clears it"""
        print("SEND PACKETS")
        copied_packets = self.packets_to_send
        self.packets_to_send = []
        # [print(copied_packets)
        for packet in copied_packets:
            if packet[0] == ID_DIRECTIONCOMMAND or packet[0] == "*heartbeat*":
                pass
                print(f"{packet = }")
        if run_network:
            self.logger.data_logger.info(copied_packets)
        if self.network_handler is None or not copied_packets:
            return
        self.network_handler.send(network_format(copied_packets))

    def reset_5V_fuse(self, fuse_number):
        """reset_5V_fuse creates and adds
        packets for resetting a fuse on the ROV"""
        byte0 = 0b10000000 | (fuse_number << 1)
        fuse_reset_signal = [byte0]

        for item in self.regulator_active:
            fuse_reset_signal.append(item)

        self.packets_to_send.append(97, fuse_reset_signal)
    
    def reset_5V_fuse2(self):
        reset_fuse_byte = [0] * 8
        reset_fuse_byte[0] = 1
        print("Det går inn i funksjonen")
        self.packets_to_send.append([97, reset_fuse_byte])
        print(f"Pakkene som blir sendt er: {self.packets_to_send}")
        
    def reset_12V_thruster_fuse(self, fuse_number):
        """reset_fuse_on_power_supply creates and adds
        packets for resetting a fuse on the ROV"""
        byte0 = 0b10000000 | (fuse_number << 1)
        fuse_reset_signal = [byte0]

        for item in self.regulator_active:
            fuse_reset_signal.append(item)

        self.packets_to_send.append([98, fuse_reset_signal])

    def reset_12V_manipulator_fuse(self, fuse_number):
        """reset_12V_manipulator_fuse creates and adds
        packets for resetting a fuse on the ROV"""
        byte0 = 0b10000000 | (fuse_number << 1)
        fuse_reset_signal = [byte0]

        for item in self.regulator_active:
            fuse_reset_signal.append(item)

        self.packets_to_send.append([99, fuse_reset_signal])

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
        #Kan også endre til to indexer i data listen for mani inn og ut (f.eks 0 og 1 = btn 12 og 13)
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]
        data[0] = self.data["mani_buttons"][MANIPULATOR_IN_OUT]*100
        data[1] = self.data["mani_joysticks"][MANIPULATOR_ROTATION]
        data[2] = self.data["mani_joysticks"][MANIPULATOR_TILT]
        data[3] = self.data["mani_joysticks"][MANIPULATOR_GRAB_RELEASE]
        self.packets_to_send.append([41, data])
        # print(self.packets_to_send)

    def button_handling(self):
        rov_buttons = self.data.get("rov_buttons")
        mani_buttons = self.data.get("mani_buttons")
        # print(f"KNAPPER {rov_buttons} : {mani_buttons}")
    #TODO: Add GUI commands here
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


def run(network_handler: Network, t_watch: Threadwatcher, id: int, queue_for_rov: multiprocessing.Queue,gui_pipe, frame_pipe):
    print("Klarer å gå inn i run function")
    rov_state = Rov_state(queue_for_rov, network_handler,gui_pipe, t_watch)

    # Komm. del
    print("run thread")
    print(f"{network_handler = }")
    rov_state = Rov_state(queue_for_rov, network_handler, gui_pipe,t_watch)
    print(f"{network_handler = }")
    if not network_handler == None:
        id = t_watch.add_thread()
        threading.Thread(target=rov_state.receive_data_from_rov, args=(
            network_handler, t_watch, id), daemon=True).start()
    if run_craft_packet:
        id = t_watch.add_thread()
        threading.Thread(target=rov_state.craft_packet,
                        args=(t_watch, id), daemon=True).start()
    # Con. del
    print("Before whiles")
    while t_watch.should_run(id):
        rov_state.get_from_queue()
        if run_get_controllerdata and rov_state.data != {}:
            rov_state.check_controls()
        rov_state.send_packets()
        print(":: Data sent ::")
        rov_state.data = {}

def test_gui_leak_response(gui_pipe: multiprocessing.Pipe):
    sensordata = {"lekk_temp": [False,  False, False, -1, -1, -1]}
    gui_pipe.send(sensordata)


if __name__ == "__main__":

    try:
        global run_gui
        global run_network
        global network
        global run_craft_packet
        global run_camera
        
        # exec = ExecutionClass()
        # cam = Camera()
        run_camera = True
        run_gui=True
        run_craft_packet = False
        run_network = False  # Bytt t True når du ska prøva å connecte.
        run_get_controllerdata = False
        run_send_fake_sensordata=True#Sett til True om du vil sende fake sensordata til gui
        
        t_watch = Threadwatcher()
        queue_for_rov = multiprocessing.Queue()
        
        (frame_parent_pipe, frame_chid_pipe) = Pipe()
        (
            gui_parent_pipe,#Used by main process, to send/receive data to gui
            gui_child_pipe,#Used by gui process, to send/receive data to main
        ) = Pipe()  # starts the gui program. gui_parent_pipe should get the sensor data
        
        
        #HUSK Å ENDRE TICK HVIS INPUT OPPDATERES SENT!
        debug_all = True  # Sett til True om du vil se input fra controllers

        network = False
        if run_network:
            network = Network(is_server=False, port=6900, bind_addr="0.0.0.0",
                            connect_addr="10.0.0.2")
            print("network started")
            run_network = True

            print("starting send to rov")
            id = t_watch.add_thread()
            print(id)
            main_driver_loop = threading.Thread(target=run, args=(
                network, t_watch, id, queue_for_rov,gui_parent_pipe, frame_parent_pipe), daemon=True)
            main_driver_loop.start()

        if run_get_controllerdata:
            id = t_watch.add_thread()
            # takes in controller data and sends it into child_conn
            controller_process = Process(target=controller.run, args=(
                queue_for_rov, t_watch, id, True, debug_all), daemon=True)
            controller_process.start()
            input("Press Enter to start sending!")
            # controller_process.terminate()
            
        if run_gui:
            id = t_watch.add_thread()
            gui_loop = Process(
                target=gui.run,
                args=(gui_child_pipe, queue_for_rov, t_watch, id),
                daemon=True,
            )  #should recieve commands from the gui
            gui_loop.start()
            print("gui started")
            

        if run_camera:
            id = t_watch.add_thread()
            camera_thread = threading.Thread(target=run_camera_func, args=(t_watch, frame_parent_pipe,id), daemon=True)
            camera_thread.start()

        if run_send_fake_sensordata:
            id = t_watch.add_thread()
            datafaker = threading.Thread(
                target=send_fake_sensordata,
                args=(t_watch, gui_parent_pipe),
                daemon=True,
            )
            datafaker.start()
            
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        t_watch.stop_all_threads()
        print("stopped all threads")
      