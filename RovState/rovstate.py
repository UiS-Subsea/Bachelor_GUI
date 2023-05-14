import json
from Kommunikasjon.packet_info import Logger
from RovState.network_formatter import network_format
from Thread_info import Threadwatcher
from Kommunikasjon.network_handler import Network

MANIPULATOR_IN_OUT = 15
MANIPULATOR_ROTATION = 0
MANIPULATOR_TILT = 4
MANIPULATOR_GRAB_RELEASE = 6


REGULERINGSKNAPPAR = "32"  # 0=All regulering deaktivert, 1=Aktiver rull reg, 2=Regulering av dybde aktivert, 3=Regulering av vinkel aktivert, 4=Regulering av dybde og vinkel aktivert
THRUST = "129"  # HHF, #HHB, #HVB, HVF, VHF, VHB, VVB, VVF
REGULERINGTEMP = "130"  # 0Reguleringskort, 1=Motordriverkort 2= Dybde SP
VINKLER = "138"  # 0=roll, 1=stamp, 2=gir?
DYBDETEMP = "139"  # 0=dybde, 2=vanntemp, 4=sensorkorttemp
FEILKODE = "140"  # 0=IMU Error, 1=Temp Error, 2=Trykk Error, 3=Lekkasje
TEMPKOMKONTROLLER = "145"  # =Temp
MANIPULATOR12V = "150"  # Strømtrekk, Temperatur, Sikringsstatus
THRUSTER12V = "151"  # Strømtrekk, Temperatur, Sikringsstatus
KRAFT5V = "152"  # Strømtrekk, Temperatur, Sikringsstatus


VALIDCOMMANDS = [
    THRUST,
    REGULERINGTEMP,
    VINKLER,
    DYBDETEMP,
    FEILKODE,
    TEMPKOMKONTROLLER,
    MANIPULATOR12V,
    THRUSTER12V,
    KRAFT5V,
]

# ROV
X_AXIS = 1
Y_AXIS = 0
Z_AXIS = 6
ROTATION_AXIS = 3

FRONT_LIGHT_ID = 98
BOTTOM_LIGHT_ID = 99

front_light_intensity = 0
bottom_light_intensity = 0


ID_DIRECTIONCOMMAND_PARAMETERS = 71
ID_DIRECTIONCOMMAND = 70
ID_camera_tilt_upwards = 200
ID_camera_tilt_downwards = 201


class Rov_state:
    def __init__(
        self,
        queue_for_rov,
        network_handler,
        gui_queue,
        manual_flag,
        t_watch: Threadwatcher,
    ) -> None:
        # Threadwatcher
        self.t_watch: Threadwatcher = t_watch
        self.data: dict = {}
        self.logger = Logger()
        self.manual_flag = manual_flag

        # Queues
        self.queue_for_rov = queue_for_rov
        self.gui_queue = gui_queue
        self.sensordata = None

        # Network handler that sends data to rov (and recieves)
        self.network_handler: Network = network_handler
        self.packets_to_send = []
        self.valid_gui_commands = VALIDCOMMANDS

    def update(self):
        pass

    def send_sensordata_to_gui(self, data):
        # Sends sensordata to the gui
        self.gui_queue.put(data)

    def receive_data_from_rov(self, t_watch: Threadwatcher, id: int):
        incomplete_packet = ""
        print("recive data thread")
        while t_watch.should_run(id):
            try:
                data = self.network_handler.receive()
                if data == b"" or data is None:
                    continue
                else:
                    if data is None:
                        continue
                    decoded, incomplete_packet = Rov_state.decode_packets(
                        data, incomplete_packet
                    )
                if decoded == []:
                    continue
                for message in decoded:
                    self.handle_data_from_rov(message)

                    # potentially for the future to get information to the GUI : send_to_gui(Rov_state, message)

            except json.JSONDecodeError as e:
                print(f"{data = }, {e = }")
                pass

    # Decodes the tcp packet/s recieved from the rov

    def decode_packets(tcp_data: bytes, end_not_complete_packet="") -> list:
        end_not_complete_packet = ""
        try:
            json_strings = end_not_complete_packet + bytes.decode(tcp_data, "utf-8")
            # pakken er ikke hel. Dette skal aldri skje sÃ¥ pakken burde bli forkasta
            if not json_strings.startswith('"*"'):
                return [], ""
            if not json_strings.endswith('"*"'):  # pakken er ikke hel
                end_not_complete_packet = json_strings[json_strings.rfind("*") - 1 :]
                # fjerner den ukomplette pakken. til, men ikke med indexen
                json_strings = json_strings[: json_strings.rfind("*") - 1]

            json_list = json_strings.split(json.dumps("*"))
        except Exception as e:
            print(f"{tcp_data = } Got error {e}")
            return []
        decoded_items = []

        for item in json_list:
            if item == "" or item == json.dumps("heartbeat"):
                continue

            else:
                try:
                    item = json.loads(item)
                except Exception as e:
                    print(f"{e = }\n {item = }, {tcp_data = }")
                    with open("errors.txt", "ab") as f:
                        f.write(tcp_data)
                    continue

                    # exit(0)
                decoded_items.append(item)
        return decoded_items, end_not_complete_packet

    def handle_data_from_rov(self, message: dict):
        # print(message)
        self.logger.data_logger.info(message)
        message_name = ""
        if not isinstance(message, dict):
            try:
                return
            except Exception as e:
                return
        if "Error" in message or "info" in message:  # den og
            pass
            return
        if "Alarm" in message:
            pass
        try:
            message_name = list(message.keys())[0]
        except Exception as e:
            return
        if message_name in self.valid_gui_commands:
            self.send_sensordata_to_gui(message)
        else:
            pass

    def craft_packet(self, t_watch: Threadwatcher, id):
        print("CraftPack Thread")
        while t_watch.should_run(id):
            userinput = input(
                "Packet: [parameter_id of type int, value of type float or int]: "
            )
            var = []
            try:
                var = json.loads(userinput)
                if not isinstance(var[0], int):
                    print("Error: parameter id was not an int! try again.")
                    continue
                if len(var) != 2:
                    continue
            except Exception as e:
                print(f"Error when parsing input\n {e}")
                continue
            print(var)
            self.packets_to_send.append([var[0], var[1]])

    def send_packets_to_rov(self, t_watch: Threadwatcher, id):
        while t_watch.should_run(id):
            self.get_from_queue()

            self.build_packets()

            if self.packets_to_send != []:
                self.send_packets()
                self.data = {}

    def send_packets(self):
        """Sends the created network packets and clears it"""
        copied_packets = self.packets_to_send
        self.packets_to_send = []
        for packet in copied_packets:
            if packet[0] == ID_DIRECTIONCOMMAND or packet[0] == "*heartbeat*":
                pass
        self.logger.data_logger.info(copied_packets)
        if self.network_handler is None or not copied_packets:
            return
        self.network_handler.send(network_format(copied_packets))

    def build_rov_packet(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["rov_joysticks"][X_AXIS]
        data[1] = self.data["rov_joysticks"][Y_AXIS]
        data[2] = self.data["rov_joysticks"][Z_AXIS]
        data[3] = -self.data["rov_joysticks"][ROTATION_AXIS]

        self.packets_to_send.append([33, data])

    def build_autonom_packet(self):
        if self.data == {}:
            return

        print(self.data["autonomdata"], "autonomdata")
        data = [0, 0, 0, 0, 0, 0, 0, 0]
        data[0] = self.data["autonomdata"][0]
        data[1] = self.data["autonomdata"][1]
        data[2] = self.data["autonomdata"][2]
        data[3] = self.data["autonomdata"][3]
        self.packets_to_send.append([33, data])

    def build_manipulator_packet(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]
        try:
            data[0] = self.data.get("mani_dpad", [0, 0])[1] * 100
            data[1] = self.data["mani_joysticks"][MANIPULATOR_ROTATION]
            data[2] = -self.data["mani_joysticks"][MANIPULATOR_TILT]
            data[3] = self.data["mani_joysticks"][MANIPULATOR_GRAB_RELEASE]
        except KeyError:
            pass
        self.packets_to_send.append([34, data])

    def build_reset_packet(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["reset_controls"][0]

        self.packets_to_send.append([97, data])

    def build_reset_thruster_packet(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["reset_controls_thruster"][0]

        self.packets_to_send.append([98, data])

    def build_reset_manipulator_packet(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["reset_controls_manipulator"][0]

        self.packets_to_send.append([99, data])

    def build_reset_depth(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["reset_depth"][0]

        self.packets_to_send.append([66, data])

    def build_reset_angles(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["reset_angles"][0]

        self.packets_to_send.append([66, data])

    def build_calibrate_IMU(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["kalibrer_IMU"][0]

        self.packets_to_send.append([66, data])

    def build_regulator_tuning(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["update_regulator_tuning"][0]
        data[1] = self.data["update_regulator_tuning"][1]

        self.packets_to_send.append([42, data])

    def build_toggle_regulator_all(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["toggle_regulator_all"][0]
        data[0] = self.data["toggle_regulator_all"][0]
        data[0] = self.data["toggle_regulator_all"][0]
        data[0] = self.data["toggle_regulator_all"][0]

        self.packets_to_send.append([32, data])

    def build_rull_regulator(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["toggle_rull_reg"][0]

        self.packets_to_send.append([32, data])

    def build_stamp_reg(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["toggle_stamp_reg"][0]

        self.packets_to_send.append([32, data])

    def build_dybde_regulator(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["toggle_dybde_reg"][0]

        self.packets_to_send.append([32, data])

    def build_front_light_on(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["front_light_on"][0]

        self.packets_to_send.append([98, data])

    def build_bottom_light_on(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[0] = self.data["bottom_light_on"][0]

        self.packets_to_send.append([99, data])

    def build_front_light_intensity(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[1] = self.data["slider_top_light"][1]

        self.packets_to_send.append([98, data])

    def build_bottom_light_intensity(self):
        if self.data == {}:
            return
        data = [0, 0, 0, 0, 0, 0, 0, 0]

        data[1] = self.data["slider_bottom_light"][1]

        self.packets_to_send.append([99, data])

    def build_camera_tilt(self):
        if self.data == {}:
            return
        data = self.data["tilt"]
        # print(data)

        self.packets_to_send.append([200, ["tilt", data]])

    def button_handling(self):
        rov_buttons = self.data.get("rov_buttons")
        mani_buttons = self.data.get("mani_buttons")

    def get_from_queue(self):
        """Takes data from the queue and sends it to the correct handler"""
        self.packet_id = -1
        packet = ""
        try:
            self.packet_id, packet = self.queue_for_rov.get()
            # self.packets_to_send.append(packet[0], packet[1])
            # return packet
        except Exception as e:
            return

        self.data = packet

    def build_packets(self):
        if self.packet_id == 1 and self.manual_flag.value == 1:
            # self.button_handling()
            self.build_rov_packet()
            self.build_manipulator_packet()
        elif self.packet_id == 2 and self.manual_flag.value == 0:
            self.build_autonom_packet()
        elif self.packet_id == 4:
            self.build_reset_packet()
        elif self.packet_id == 5:
            self.build_reset_thruster_packet()
        elif self.packet_id == 6:
            self.build_reset_manipulator_packet()
        elif self.packet_id == 7:
            self.build_reset_depth()
        elif self.packet_id == 8:
            self.build_reset_angles()
        elif self.packet_id == 9:
            self.build_calibrate_IMU()
        elif self.packet_id == 10:
            self.build_regulator_tuning()
        elif self.packet_id == 11:
            self.build_toggle_regulator_all()
        elif self.packet_id == 12:
            self.build_rull_regulator()
        elif self.packet_id == 13:
            self.build_stamp_reg()
        elif self.packet_id == 14:
            self.build_dybde_regulator()
        elif self.packet_id == 15:
            self.build_front_light_on()
        elif self.packet_id == 16:
            self.build_bottom_light_on()
        elif self.packet_id == 17:
            self.build_front_light_intensity()
        elif self.packet_id == 18:
            self.build_bottom_light_intensity()
        elif self.packet_id == 19:
            self.build_camera_tilt()

        # print(self.packets_to_send)
