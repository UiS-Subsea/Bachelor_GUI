from multiprocessing import Pipe, Process, Queue
import threading
from network_handler import Network
import json
from Thread_info import Threadwatcher
import multiprocessing
import time
#from logger import Logger


class Rov_state:
    def __init__(self, queue, network_handler, gui_pipe, t_watch: Threadwatcher) -> None:
        print("rov state thread")
        self.t_watch: Threadwatcher = t_watch
        self.data: dict = {}
        self.queue: multiprocessing.Queue = queue
        # Pipe to send sensordata back to the gui
        self.gui_pipe = gui_pipe
        # Network handler that sends data to rov (and recieves)
        self.network_handler: Network = network_handler

    def recieve_data_from_rov(self, network: Network, t_watch: Threadwatcher, id: int):
        incomplete_packet = ""
        print("recive data thread")
        while t_watch.should_run(id):
            try:
                data = network.receive()
                if data == b"" or data is None:
                    continue
                else:
                    print(data)
                # if data is None:
                #    continue
                    decoded, incomplete_packet = Rov_state.decode_packets(
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
            json_strings = end_not_complete_packet + \
                bytes.decode(tcp_data, "utf-8")
            print(json_strings)
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
            # self.logger.sensor_logger.info(message)
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

    def network_format(data) -> bytes:
        """Formats the data for sending to network handler"""
        packet_seperator = json.dumps("*")
        return bytes(packet_seperator+json.dumps(data)+packet_seperator, "utf-8")


def run(network_handler: Network, t_watch: Threadwatcher, id: int, queue_for_rov: multiprocessing.Queue, gui_pipe):
    print("run thread")
    print(f"{network_handler = }")
    rov_state = Rov_state(queue_for_rov, network_handler, gui_pipe, t_watch)
    print(f"{network_handler = }")
    if not network_handler == None:
        id = t_watch.add_thread()
        threading.Thread(target=rov_state.recieve_data_from_rov, args=(
            network_handler, t_watch, id), daemon=True).start()


if __name__ == "__main__":

    try:
        global run_network
        global network
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
