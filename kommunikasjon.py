# todo test if all datatypes is converted correctly
import can
import struct
import time
import json
import threading
from network_handler import Network

can_types = {
    "int8": ">b",
    "uint8": ">B",
    "int16": ">h",
    "uint16": ">H",
    "int32": ">i",
    "uint32": ">I",
    "int64": ">q",
    "uint64": ">Q",
    "float": ">f"
}
#lage skjema med manip.

#[id,[x,y,z]] <-- eksempel på en pakke vi kan sendte (x frem fra rov perspektiv), y opp, z ned
#[54,[]]
#[55,[20]] <- bruker 20% kraft av manipula.


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
    canID, *idData = tags
    idDataByte = []
    for data in idData:
        try:
            idDataByte += struct.pack(can_types[data[0]], *data[1:])
        except struct.error as e:
            print(f"Error: {e}")
            print(f"data={data}, format={data[0]}, value={data[1:]}")
            print(f"idDataByte={idDataByte}")

    return can.Message(arbitration_id=canID, data=idDataByte, is_extended_id=False)

# decodes packs

#sendte samme id, ikkje som canbus, men som lite. 
#der første tallet høyrte til canbus id'en.
def packetDecode(msg):
    canID = msg.arbitration_id
    dataByte = msg.data
    if canID == 100:
        pack1 = get_num("int16", dataByte[0:2])
        pack2 = get_num("int16", dataByte[2:4])
        pack3 = get_num("int16", dataByte[4:6])
        pack4 = get_num("int16", dataByte[6:8])
        json_dict = {"name10": (pack1, pack2, pack3, pack4)}
    elif canID == 52:
        pack1 = get_num("int32", dataByte[0:4])
        pack2 = get_num("int8",  dataByte[4])
        pack3 = get_num("uint8", dataByte[5])
        pack4 = get_num("uint16", dataByte[6:8])
        json_dict = {"name52": (pack1, pack2, pack3, pack4)}
    else:
        return f"Unknown CanID: {canID} recived from ROV system"
    return to_json(json_dict)

# class for esatblishing canbus interface, sending and reciving messages
# initialise with Canbus()
# method .sendPacket(tag) to send
# method .readPacket() to read


class ComHandler:
    def __init__(self,
                 ip: str = '0.0.0.0',
                 port: int = 5010,
                 canifaceType: str = 'socketcan',
                 canifaceName: str = 'can0') -> None:
        self.canifaceType = canifaceType
        self.canifaceName = canifaceName
        self.status = {'Net': False, 'Can': False}
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
        self.toggleNet

    def toggleNet(self):
        if self.status['network']:
            # This will stop network thread
            self.status['network'] = False
        else:
            self.network_trad = threading.Thread(name="Network_thread", target=network_thread, daemon=True, args=(
                self.network_handler, self.network_callback, self.status))
            self.network_trad.start()

    def canInit(self):
        self.bus = can.Bus(
            interface=self.ifacetypeCan,
            channel=self.ifacenameCan,
            receive_own_messages=False,
            fd=False)
        #self.listner = can.Listener()
        self.notifier = can.Notifier(self.bus, [self.readPacket])
        self.timeout = 0.1  # todo kan denne fjernes?

    def sendPacket(self, tag):
        packet = packetBuild(tag)
        assert self.bus is not None
        try:
            self.bus.send(packet)
        except Exception as e:
            raise e

    def readPacket(self, can):
        self.bus.socket.settimeout(0)
        return f"{packetDecode(can)}"


if __name__ == "__main__":
    # tag = (type, value)
    tag0 = ("int16", 16550)
    tag1 = ("int8", 120)
    tag2 = ("uint8", 240)
    tag3 = ("uint16", 50000)
    tag4 = ("int16", -20000)
# tags = (id, tag0, tag1, tag2, tag3, tag4, tag5, tag6, tag7) ex. with int8 or uint8
    tags = (10, tag0, tag1, tag2, tag3, tag4)
    c = ComHandler()
    while True:
        c.sendPacket(tags)
