from multiprocessing import Pipe, Process, Queue
from network_handler import Network
import json
from Thread_info import Threadwatcher

def recieve_data_from_rov(self, network: Network, t_watch: Threadwatcher, id: int):
        incomplete_packet = ""
        while t_watch.should_run(id):
            try:
                data = network.receive()
                # print(data)
                if data is None:
                    continue
                decoded, incomplete_packet = decode_packets(data, incomplete_packet)
                if decoded == []:
                    continue

                for message in decoded:
                    # print(message)
                    self.handle_data_from_rov(message)

                    # Rov_state.send_sensordata_to_gui(Rov_state, message)

            except json.JSONDecodeError as e:
                print(f"{data = }, {e = }")
                pass


# Decodes the tcp packet/s recieved from the rov
def decode_packets(tcp_data: bytes, end_not_complete_packet="") -> list:
    end_not_complete_packet = ""
    try:
        json_strings = end_not_complete_packet+bytes.decode(tcp_data, "utf-8")

        if not json_strings.startswith('"*"'): # pakken er ikke hel. Dette skal aldri skje så pakken burde bli forkasta
            #print(f"Packet did not start with '*' something is wrong. {end_not_complete_packet}")
            return [], ""
        if not json_strings.endswith('"*"'): # pakken er ikke hel
            end_not_complete_packet = json_strings[json_strings.rfind("*")-1:]
            json_strings = json_strings[:json_strings.rfind("*")-1] # fjerner den ukomplette pakken. til, men ikke med indexen

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