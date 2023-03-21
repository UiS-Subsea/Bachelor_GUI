from multiprocessing import Pipe, Process, Queue
import threading
from network_handler import Network
import json
from Thread_info import Threadwatcher
import multiprocessing
import time
from packet_info import Logger

#from logger import Logger
ID_DIRECTIONCOMMAND_PARAMETERS = 71
ID_DIRECTIONCOMMAND = 70
ID_camera_tilt_upwards = 200
ID_camera_tilt_downwards = 201

# takes a python object and prepares it for sending over network

# HUSK Å LEGGE TIL COMMENTS!


def network_format(data) -> bytes:
    """Formats the data for sending to network handler"""
    packet_seperator = json.dumps("*")
    return bytes(packet_seperator+json.dumps(data)+packet_seperator, "utf-8")


class Rov_state:
    def __init__(self, queue, network_handler, gui_pipe, t_watch: Threadwatcher) -> None:
        print("rov state thread")
        self.t_watch: Threadwatcher = t_watch
        self.data: dict = {}
        self.logger = Logger()
        self.queue: multiprocessing.Queue = queue
        # Pipe to send sensordata back to the gui
        self.gui_pipe = gui_pipe
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

    def recieve_data_from_rov(self, network: Network, t_watch: Threadwatcher, id: int):
        incomplete_packet = ""
        print("recive data thread")
        while t_watch.should_run(id):
            try:
                data = network.receive()
                if data == b"" or data is None:
                    continue
                else:
                    # print(data)
                    # if data is None:
                    #    continue
                    decoded, incomplete_packet = Rov_state.decode_packets(
                        data, incomplete_packet)
                if decoded == []:
                    continue
                for message in decoded:
                    # print(message)
                    self.handle_data_from_rov(message)

                    # potentially for the future to get information to the GUI : send_to_gui(Rov_state, message)

            except json.JSONDecodeError as e:
                print(f"{data = }, {e = }")
                pass

    # Decodes the tcp packet/s recieved from the rov

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
            self.logger.sensor_logger.info(message)
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
        except Exception as e:
            print(e)
            return
        else:
            pass
            print(f"\n\nMESSAGE NOT RECOGNISED\n{message}\n")

    def network_format(data) -> bytes:
        """Formats the data for sending to network handler"""
        packet_seperator = json.dumps("*")
        return bytes(packet_seperator+json.dumps(data)+packet_seperator, "utf-8")

    def craft_packet(self, t_watch: Threadwatcher, id):
        print("CraftPack Thread")
        while t_watch.should_run(id):
            userinput = input(
                "Packet: [parameter_id of type int, value of type float or int]: ")
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
            print(var)
            #self.packets_to_send.append([ID_DIRECTIONCOMMAND_PARAMETERS, var])
            self.packets_to_send.append([var[0], var[1]])

    def send_packets(self):
        """Sends the created network packets and clears it"""

        copied_packets = self.packets_to_send
        self.packets_to_send = []
        # [print(copied_packets)
        for packet in copied_packets:
            if packet[0] == ID_DIRECTIONCOMMAND or packet[0] == "*heartbeat*":
                pass
                print(f"{packet = }")
        if run_network:
            self.logger.sensor_logger.info(copied_packets)
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


    def update_light_value(self, light_intensity_forward: int, ligth_forward_is_on: bool, light_intensity_down: int, ligth_down_is_on: bool):
        self.light_intensity_forward = light_intensity_forward
        self.ligth_forward_is_on = ligth_forward_is_on

        self.light_intensity_down = light_intensity_down
        self.ligth_down_is_on = ligth_down_is_on

        ligth_down = self.light_intensity_down * self.ligth_down_is_on
        ligth_forward = self.light_intensity_forward * self.ligth_forward_is_on
        # print(f"Lys oppdatert. verdien vi sender er {[142, ligth_forward, ligth_down]}")
        self.packets_to_send.append([ID_LIGHTS, [ligth_forward, ligth_down]])
        #send id også light_dim_value


    # def reset_12V_manipulator_fuse(self, fuse_number):
    #     """reset_12V_manipulator_fuse creates and adds
    #     packets for resetting a fuse on the ROV"""
    #     byte0 = 0b01000000 | (fuse_number << 1)
    #     fuse_reset_signal = [byte0]
    #     for item in self.regulator_active:
    #         fuse_reset_signal.append(item)
    #     self.packets_to_send.append([139, fuse_reset_signal])

    # def reset_12V_manipulator_fuse(self):
    #     """reset_12V_manipulator_fuse creates and adds
    #     packets for resetting a fuse on the ROV"""
    # #      fuset_reset_signal = [True] + [False] * 7 
    # #      self.packets_to_send.append([99, fuse_reset_signal])
    #     fuse_reset_signal = [False] * 8
    #     fuse_reset_signal[0] = True

        

    # def reset_12V_thruster_fuse(self, fuse_number):
    #     """reset_12V_thruster_fuse creates and adds
    #     packets for resetting a fuse on the ROV"""
    #     byte,
    # # def reset_12V_thruster_fuse(self, fuse_number):
    #     # Resets 12V thruster fuse using 98 id


def run(network_handler: Network, t_watch: Threadwatcher, id: int, queue_for_rov: multiprocessing.Queue, gui_pipe):
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
        global run_network
        global network
        global run_craft_packet
        run_craft_pakcet = True
        run_network = False

        queue_for_rov = multiprocessing.Queue()
        t_watch = Threadwatcher()

        gui_parent_pipe, gui_child_pipe = Pipe()

        network = None
        if not run_network:
            network = Network(is_server=False, port=6900, bind_addr="0.0.0.0",
                              connect_addr="10.0.0.2")
            print("network started")
            run_network = True

        print("starting send to rov")
        id = t_watch.add_thread()
        print(id)
        main_driver_loop = threading.Thread(target=run, args=(
            network, t_watch, id, queue_for_rov, gui_parent_pipe), daemon=True)
        main_driver_loop.start()

        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        t_watch.stop_all_threads()
        print("stopped all threads")


# Pakke Oppsett
# [id, [f, o, n]] # Pakke for styring, f-frem, o-opp, n-ned
# [50, [20]] <-- Hvor mye kraft manipulatoren skal bruke
