from ast import arg
from json.tool import main
from mimetypes import init
from multiprocessing import context
from unicodedata import name
from xml.etree.ElementInclude import include
import threading
#import cv2
import time
#import serial
import json
import socket

#lag en egen klasse som har oversikt over alle packets. 

# Test function for socket connection
def venus(ip, port, meld):
    network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # network_socket.settimeout(5)
    network_socket.connect((ip, port))
    print("connected")
    for __ in range(10):
        time.sleep(0.001)
        try:
            network_socket.sendall(str.encode(meld))
        except:
            print("Connection lost")
            break
    # network_socket.sendall(b"END")
    network_socket.close()

# Reads data from network port
def network_thread(network_socket, network_callback, flag):
    #network_socket.bind("tcp://127.0.0.1:6892")
    print("Server started\n")
    while flag[0]:
        melding = network_socket.recv(1024)
        if melding == b"END":
            break
        else:
            network_callback(melding)
    network_socket.close()
    print(f'Thread stopped')

# Reads serial data
def USB_thread(h_serial, USB_callback, flag):
    while flag[1]:
        try:
            melding = h_serial.readline().decode("utf8").strip("\n")
            USB_callback(melding)
        except:
            pass
    print("USB thread stopped")

class Callbacks:
    def __init__(self) -> None:
        # Flags
        self.network_status = False
        self.USB_status = False
        self.status_flag_list = [1,1,1,1,1] # Index 0 = Network, Index 1 = USB, Index 3 = ?, index 4 = ?
        self.connect_ip = "127.0.0.1"
        self.connect_port = 6899
        self.net_init()
        


    def net_init(self):
        self.network_rcv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.network_rcv_socket.bind((self.connect_ip, self.connect_port))
        self.network_rcv_socket.settimeout(5)
        self.network_rcv_socket.listen()
        self.network_connection, self.network_address = self.network_rcv_socket.accept()


    def network_callback(self, message):
        #self.serial.write(message)
        print(message)

    def toggle_network(self):
        if self.network_status:
            self.status_flag_list = 0
            self.network_status = False
        else:
            print("Starting thread")
            self.network_trad = threading.Thread(name="Network_thread",target=network_thread, daemon=True, args=(self.network_connection, self.network_callback, self.status_flag_list))
            self.network_trad.start()
            self.network_status = True

    def USB_callback(self, melding):
        self.network_snd_socket(melding)


    def toggle_USB(self):
        if self.USB_status:
            self.status_flag_list[1] = 0
            time.sleep(2)
            self.serial.close()
            self.USB_status = False
        else:
            self.serial = serial.Serial(self.serial_port, self.serial_baud, timeout=1)
            self.serial.write(b"t")
            self.serial_thread = threading.Thread(name = "Serial_thread", target=USB_thread, daemon=True, args=(self.serial, self.USB_callback, self.status_flag_list))
            self.serial_thread.start()
            self.USB_status = True


if __name__ == "__main__":
    dictionary = {"CAN":1, "camera": 1}
    meld = json.dumps(dictionary)
    ip = "10.0.0.2"
    port = 6900
    venus_trad = threading.Thread(name="venus", target=venus, args=(ip, port, meld))
    venus_trad.start()
    # a = Callbacks()
    # a.toggle_network()
    print("For loop started")
    for __ in range(4):
        time.sleep(1)
    print("For loop stopped")