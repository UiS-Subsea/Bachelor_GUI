import argparse
import logging
import json
import socket
import threading
import time

# Kode er rewritet, mange linjer er slettet og noen ting er byttet fra den
# originale delen.

# Filen setter opp flere threads til å "overlook" socket connection og kommunikasjon

# Venus funksjonen sender informasjon til en socket tilkobling.


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

# NetworkThread klassen venter og "sender" socket informasjonen til
# Callback klassen som får den informasjonen/dataen opp.
# Klassen høyrer etter informasjonen,


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


class Callbacks:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.network_status = False
        self.flag = [1, 1, 1, 1, 1]
        self.network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.network_socket.bind((self.ip, self.port))
        self.network_socket.settimeout(5)
        self.network_socket.listen()
        self.connection, self.address = self.network_socket.accept()
        self.network_thread = NetworkThread(
            self.connection, self.network_callback, self.flag)

# Printer informasjonen som blei fått fra network connection
    def network_callback(self, message):
        logging.info("Received message: %s", message)

# Toggle_network funksjonen enten starter eller stopper netowrk threads
# basert på connection state
    def toggle_network(self):
        if self.network_status:
            self.flag[0] = 0
            self.network_status = False
        else:
            logging.info("Starting network thread")
            self.network_thread.start()
            self.network_status = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test socket connection")
    parser.add_argument("--ip", type=str)
