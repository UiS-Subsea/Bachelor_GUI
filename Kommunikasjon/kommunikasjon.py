# todo test if all datatypes is converted correctly
import can
import struct
import time
import json
import threading
import sys
import os
import subprocess
from network_handler import Network


can_types = {
    "int8": "<b",
    "uint8": "<B",
    "int16": "<h",
    "uint16": "<H",
    "int32": "<i",
    "uint32": "<I",
    "int64": "<q",
    "uint64": "<Q",
    "float": "<f"
}


def get_byte(can_format: str, number):
    return list(struct.pack(can_types[can_format], number))


def get_num(can_format: str, byt):
    if isinstance(byt, int):
        byt = byt.to_bytes(1, byteorder="big")
    return struct.unpack(can_types[can_format], byt)[0]


def get_bit(num, bit_nr):
    return (num >> bit_nr) & 1


def set_bit(bits: tuple):
    return sum(bit << k for k, bit in enumerate(bits))
# formats to json


def to_json(input):
    packet_sep = json.dumps("*")
    return bytes(packet_sep + json.dumps(input) + packet_sep, "utf-8")

# builds packs for canbus


def packetBuild(tags):
    if tags == 'marco\n':
        pack = 'marco\n'
        pack = bytearray(pack, "utf-8")
        print(pack)
        return can.Message(arbitration_id=63, data=pack, is_extended_id=False)
    else:
        canID, *idData = tags
        idDataByte = []
        for data in idData:
            print(data)
            try:
                print(data[0])
                idDataByte += struct.pack(can_types[data[0]], *data[1:])
            except struct.error as e:
                print(f"Error: {e}")
                print(f"data={data}, format={data[0]}, value={data[1:]}")
                print(f"idDataByte={idDataByte}")
        return can.Message(arbitration_id=canID, data=idDataByte, is_extended_id=False)

# decodes packs


def packetDecode(msg):
    canID = msg.arbitration_id
    dataByte = msg.data
    print(msg)
    if 1 < canID < 150:
        pack1 = get_num("int16", dataByte[0:2])
        pack2 = get_num("int16", dataByte[2:4])
        pack3 = get_num("int16", dataByte[4:6])
        pack4 = get_num("int16", dataByte[6:8])
        json_dict = {canID: (pack1, pack2, pack3, pack4)}
    elif canID == 97:
        pack1 = get_num("int32", dataByte[0:4])
        pack2 = get_num("int8",  dataByte[4])
        pack3 = get_num("uint8", dataByte[5])
        pack4 = get_num("uint16", dataByte[6:8])
        json_dict = {canID: (pack1, pack2, pack3, pack4)}
    elif canID == 155:
        pack = dataByte[0:6].decode('utf-8')
        print(f"Polo: {pack}")
        json_dict = {canID: (pack)}
    else:
        #print(f"Unknown CanID: {canID} recived from ROV system")
        # return to_json("Unknown CanID:" {canID} "recived from ROV system")
        # return to_json({"ID unknown", "0" ,"0" ,"0"})
        return f"Unknown CanID: {canID} recived from ROV system"

    return to_json(json_dict)

# Reads data from network port


def netThread(netHandler, netCallback, flag):
    print("Server started\n")
    flag['Net'] = True
    while flag['Net']:
        try:
            melding = netHandler.receive()
            # melding = network_socket.recv(1024) #  OLD
            if melding == b"" or melding is None:
                continue
            else:
                # print(melding)
                netCallback(melding)
        except ValueError as e:
            print(f'Feilkode i network thread feilmelding: {e}\n\t{melding}')
            break
    netHandler.exit()
    print(f'Network thread stopped')


class ComHandler:
    def __init__(self,
                 ip: str = '10.0.0.2',
                 port: int = 6900,
                 canifaceType: str = 'socketcan',
                 canifaceName: str = 'can0') -> None:
        self.canifaceType = canifaceType
        self.canifaceName = canifaceName
        self.status = {'Net': False, 'Can': False}
        self.canFilters = [
            {"can_id": 0x00, "can_mask": 0x00, "extended": False}]
        # activate can in os sudo ip link set can0 type can bitrate 500000 etc.
        # check if can is in ifconfig then
        self.canInit()
        self.connectIp = ip
        self.connectPort = port
        self.netInit()

    def netInit(self):
        self.netHandler = Network(is_server=True,
                                  bind_addr=self.connectIp,
                                  port=self.connectPort)
        while self.netHandler.waiting_for_conn:
            time.sleep(1)
        self.toggleNet()

    def toggleNet(self):
        if self.status['Net']:
            # This will stop network thread
            self.status['Net'] = False
        else:
            self.netTrad = threading.Thread(name="Network_thread", target=netThread, daemon=True, args=(
                self.netHandler, self.netCallback, self.status))
            self.netTrad.start()

    def netCallback(self, data: bytes) -> None:
        data: str = bytes.decode(data, 'utf-8')
        for message in data.split(json.dumps("*")):
            try:
                if message == json.dumps('heartbeat') or message == "":
                    if message is None:
                        message = ""
                    continue
                else:
                    message = json.loads(message)
                    # print(message)
                    for item in message:
                        if item[0] < 200:
                            if self.status['Can']:
                                if item[0] == 100:
                                    print(type(item[0]))
                                    print(type(item[1][0]))
                                    msg = (item[0], ("int16", item[1][0]), ("int16", item[1][1]), (
                                        "int16", item[1][2]), ("int16", item[1][3]))
                                    self.sendPacket(msg)
                                elif item[0] == 5:
                                    msg = {item[0],
                                           {'int16', int(item[1])}, {'int16', int(item[2])}, {
                                        'int16', int(item[3])}, {'int16', int(item[4])}
                                    }
                                    self.sendPacket(msg)
                            else:
                                self.netHandler.send(
                                    to_json("Error: Canbus not initialised"))
            except Exception as e:
                print(
                    f'Feilkode i network_callback, feilmelding: {e}\n\t{message}')

# canInit bruker physical interface, må sette opp en virtual interface.
    def canInit(self):  # Endre caninit.
        try:
            # Import the necessary modules
            import os
            import subprocess
            import time

            # Create a virtual canbus interface
            os.system('sudo modprobe vcan')
            os.system('sudo ip link add dev vcan0 type vcan')
            os.system('sudo ip link set up vcan0')

            # Initialize the CAN bus
            self.bus = can.interface.Bus(
                bustype='socketcan', channel='vcan0', bitrate=self.bitrate)

            # Set the CAN filters
            self.bus.set_filters(self.canFilters)

            # Set the status
            self.status['Can'] = True

            # Set the notifier and timeout
            self.notifier = can.Notifier(self.bus, [self.readPacket])
            self.timeout = 0.1

        except Exception as e:
            print("Error initializing the CAN bus:", e)

    def sendPacket(self, tag):
        packet = packetBuild(tag)
        assert self.bus is not None
        try:
            self.bus.send(packet)
        except Exception as e:
            raise e

    def readPacket(self, can):
        self.bus.socket.settimeout(0)
        self.netHandler.send(packetDecode(can))


if __name__ == "__main__":
    # tag = (type, value)
    tag0 = ("int16", 16550)
    tag1 = ("int8", 120)
    tag2 = ("uint8", 240)
    tag3 = ("uint16", 50000)
    tag4 = ("int16", -20000)
# tags = (id, tag0
# tag1, tag2, tag3, tag4, tag5, tag6, tag7) ex. with int8 or uint8
    tags = (10, tag0, tag1, tag2, tag3, tag4)
    print(tags)
    c = ComHandler()
    while True:
        c.sendPacket('marco\n')
        time.sleep(1)
