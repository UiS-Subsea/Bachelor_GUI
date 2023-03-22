import multiprocessing
import can
import struct
import time
import json
import threading
from Kommunikasjon.network_handler import Network
from Kommunikasjon.Thread_info import Threadwatcher

class Rov_status:
    def __init__(self, queue, network_handler, gui_pipe, t_watch: Threadwatcher) -> None:
        print("rov state thread")
        self.t_watch: Threadwatcher = t_watch
        self.data:dict = {}
        self.queue: multiprocessing.Queue = queue
        # Pipe to send sensordata back to the gui
        self.gui_pipe = gui_pipe
        self.camera_tilt: float[list] = [0, 0]
        # Network handler that sends data to rov (and recieves)
        self.network_handler: Network = network_handler
        self.packets_to_send = []