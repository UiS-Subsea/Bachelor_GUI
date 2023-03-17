from multiprocessing import Pipe, Process, Queue
import threading
from network_handler import Network
import json
from Thread_info import Threadwatcher


def recieve_data_from_rov(self, network: Network, t_watch: Threadwatcher, id: int):
    incomplete_packet = ""
    while t_watch.should_run(id):
        try:
            data = network.receive()
            print(data)
            if data is None:
                continue
            
            decoded, incomplete_packet = decode_packets(
                data, incomplete_packet)
            if decoded == []:
                continue

            for message in decoded:
                # print(message)
                self.handle_data_from_rov(message)

                # potentially for the future: send_to_gui(Rov_state, message)

        except json.JSONDecodeError as e:
            print(f"{data = }, {e = }")
            pass


# Decodes the tcp packet/s recieved from the rov
#
def decode_packets(tcp_data: bytes, end_not_complete_packet="") -> list:
    end_not_complete_packet = ""
    try:
        json_strings = end_not_complete_packet+bytes.decode(tcp_data, "utf-8")
        print(json_strings)
        # pakken er ikke hel. Dette skal aldri skje så pakken burde bli forkasta
        if not json_strings.startswith('"*"'):
            #print(f"Packet did not start with '*' something is wrong. {end_not_complete_packet}")
            return [], ""
        if not json_strings.endswith('"*"'):  # pakken er ikke hel
            end_not_complete_packet = json_strings[json_strings.rfind("*")-1:]
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
    if "ERROR" in message or "info" in message:
        print(message)
        return
    try:
        message_name = list(message.keys())[0]
    except Exception as e:
        print(e)
        return
    else:
        pass
        print(f"\n\nMESSAGE NOT RECOGNISED\n{message}\n")


def craft_packet(self, t_watch: Threadwatcher, id):
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

        self.packets_to_send.append([ID_DIRECTIONCOMMAND_PARAMETERS, var])


def send_packets(self):
    """Sends the created network packets and clears it"""

    copied_packets = self.packets_to_send
    self.packets_to_send = []
    for packet in copied_packets:
        if packet[0] != ID_DIRECTIONCOMMAND:
            pass
            print(f"{packet = }")
    if run_network:
        self.logger.sensor_logger.info(copied_packets)
    if self.network_handler is None:
        return
    self.network_handler.send(network_format(copied_packets))


if __name__ == "__main__":

    global run_network
    run_network = False

    network = None
    if run_network:
        network = Network(is_server=False, port=6900, connect_addr="10.0.0.2")
        print("network started")
        t_watch = Threadwatcher()

        print("starting send to rov")
        id = t_watch.add_thread()

    main_driver_loop = threading.Thread(target=run, args=(
        network, t_watch, id, queue_for_rov, gui_parent_pipe), daemon=True)
    main_driver_loop.start()
