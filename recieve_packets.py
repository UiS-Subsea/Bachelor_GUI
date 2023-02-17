import argparse
import logging
import json
import socket
import threading
import time

# Er en Network klasse om representere en connection, Klassen har en init metoden
# som initialize flere parametere som blir brukt senere.
class Network:
    def __init__(self, is_server=False, bind_addr="127.0.0.1", port=6900, connect_addr="127.0.0.1"):
        self.is_server = is_server
        self.bind_addr = bind_addr
        self.connect_addr = connect_addr
        self.port = port
        self.conn = None
        self.running = True
        self.timeout = 0.4
        self._init_socket()
        self._start_threads()
# Initialize ein ny socket med en  reuseaddr (noe som er innebygd i socket.)
# Lagde egen funksjon for holde styr på hva som gjør hva.



def venus(ip, port, meld):
    network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    network_socket.connect((ip, port))
    logging.info("Connected to %s:%d", ip, port)
    for i in range(10):
        time.sleep(0.001)
        try:
            network_socket.sendall(str.encode(meld))
        except:
            logging.error("Connection lost")
            break
    network_socket.close()


class NetworkThread:
    def __init__(self, socket, callback, flag):
        self.socket = socket
        self.callback = callback
        self.flag = flag

    def run(self):
        while self.flag[0]:
            message = self.socket.recv(1024)
            if message == b"END":
                break
            else:
                self.callback(message)
        self.socket.close()
        logging.info("Thread stopped")
