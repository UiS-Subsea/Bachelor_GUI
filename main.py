# is empty
# testing for saving to windows kappa xd xd

import json
import multiprocessing
from Kommunikasjon.network_handler import Network
from multiprocessing import Process, Pipe
import threading
import time
from Kommunikasjon.packet_info import Logger
from Thread_info import Threadwatcher
from Controller import Controller_Handler as controller
from RovState.send_fake_sensordata import send_fake_sensordata
from RovState.rovstate import Rov_state
import gui
import os

# VALUES: (0-7) -> index i: [0,0,0,0,0,0,0,0]
# MANIPULATOR
MANIPULATOR_IN_OUT = 15
MANIPULATOR_ROTATION = 0
MANIPULATOR_TILT = 3
MANIPULATOR_GRAB_RELEASE = 6


REGULERINGSKNAPPAR = "32"  # 0=All regulering deaktivert, 1=Aktiver rull reg, 2=Regulering av dybde aktivert, 3=Regulering av vinkel aktivert, 4=Regulering av dybde og vinkel aktivert
THRUST = "129"  # HHF, #HHB, #HVB, HVF, VHF, VHB, VVB, VVF
REGULERINGTEMP = "130"  # 0Reguleringskort, 1=Motordriverkort
VINKLER = "138"  # 0=roll, 1=stamp, 2=gir?
DYBDETEMP = "139"  # 0=dybde, 2=vanntemp, 4=sensorkorttemp
FEILKODE = "140"  # 0=IMU Error, 1=Temp Error, 2=Trykk Error, 3=Lekkasje
TEMPKOMKONTROLLER = "145"  # =Temp
MANIPULATOR12V = "150"  # Strømtrekk, Temperatur, Sikringsstatus
THRUSTER12V = "151"  # Strømtrekk, Temperatur, Sikringsstatus
KRAFT5V = "152"  # Strømtrekk, Temperatur, Sikringsstatus

_tilt_downwards = 201


# # TODO: HER VAR TIDLIGARE frame_pipe


if __name__ == "__main__":
    try:
        # os.environ["QT_QPA_PLATFORM"] = "xcb"
        global run_gui
        global run_network
        global network
        global run_craft_packet
        global run_camera
        # exec = ExecutionClass()

        # cam = Camera()
        manual_flag = multiprocessing.Value("i", 1)
        run_gui = True
        run_craft_packet = False
        run_network = False  # Bytt t True når du ska prøva å connecte.
        run_get_controllerdata = False
        # Sett til True om du vil sende fake sensordata til gui
        run_send_fake_sensordata = True

        t_watch = Threadwatcher()
        queue_for_rov = multiprocessing.Queue()
        gui_queue = multiprocessing.Queue()

        debug_all = False  # Sett til True om du vil se input fra controllers

        if run_network:
            network = Network(
                is_server=False, port=6900, bind_addr="0.0.0.0", connect_addr="10.0.0.2"
            )

            rovstate = Rov_state(
                queue_for_rov, network, gui_queue, manual_flag, t_watch
            )

            id = t_watch.add_thread()
            rov_state_recv_loop = threading.Thread(
                target=rovstate.receive_data_from_rov, args=(t_watch, id), daemon=True
            )
            rov_state_recv_loop.start()

            id = t_watch.add_thread()
            rov_state_send_loop = threading.Thread(
                target=rovstate.send_packets_to_rov, args=(t_watch, id), daemon=True
            )
            rov_state_send_loop.start()

        if run_get_controllerdata:
            id = t_watch.add_thread()
            # takes in controller data and sends it into child_conn
            controller_process = Process(
                target=controller.run,
                args=(queue_for_rov, manual_flag, t_watch, id, True, debug_all),
                daemon=True,
            )
            controller_process.start()
            # controller_process.terminate()

        if run_gui:
            id = t_watch.add_thread()
            gui_loop = Process(
                target=gui.run,
                args=(gui_queue, queue_for_rov, manual_flag, t_watch, id),
                daemon=True,
            )  # should recieve commands from the gui
            gui_loop.start()

        if run_send_fake_sensordata:
            id = t_watch.add_thread()
            datafaker = threading.Thread(
                target=send_fake_sensordata,
                args=(t_watch, gui_queue),
                daemon=True,
            )
            datafaker.start()

        while True:
            # print(queue_for_rov.get())
            time.sleep(1)
    except KeyboardInterrupt:
        t_watch.stop_all_threads()
        print("stopped all threads")
