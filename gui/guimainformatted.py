import time
from Thread_info import Threadwatcher
import multiprocessing
from multiprocessing import Pipe, Process, Queue
from gui import gui
import threading


def create_test_sensordata(delta, old_sensordata=None):
    # TODO: don't use this later its a test function
    sensordata = {}
    if old_sensordata is None:
        sensordata = {"dybde": -2500.0, "spenning": 48.0, "temp_rov": 26.0}
    else:
        # sensordata["tid"] = int(time.time()-start_time_sec)
        sensordata["dybde"] = old_sensordata["dybde"] + 10 * delta
        sensordata["spenning"] = old_sensordata["spenning"] + 0.4 * delta
        sensordata["temp_rov"] = old_sensordata["temp_rov"] + 0.3 * delta
    return sensordata


def send_fake_sensordata(t_watch: Threadwatcher, gui_pipe: multiprocessing.Pipe):
    thrust_list = [num for num in range(-100, 101)]
    power_list = [num for num in range(0, 101)]
    count = -1
    sensordata = {}
    while t_watch.should_run(0):
        # time_since_start = round(time.time()-start_time_sec)
        count += 1
        sensordata["lekk_temp"] = [
            True,
            True,
            True,
            (25 + count) % 60,
            (37 + count) % 60,
            (61 + count) % 60,
        ]
        sensordata["thrust"] = [
            thrust_list[(0 + count) % 201],
            thrust_list[(13 + count) % 201],
            thrust_list[(25 + count) % 201],
            thrust_list[(38 + count) % 201],
            thrust_list[(37 + count) % 201],
            thrust_list[(50 + count) % 201],
            thrust_list[(63 + count) % 201],
            thrust_list[(75 + count) % 201],
            thrust_list[(88 + count) % 201],
            thrust_list[(107 + count) % 201],
        ]
        sensordata["power_consumption"] = [
            power_list[count % 101] * 13,
            power_list[count % 101] * 2.4,
            power_list[count % 101] * 0.65,
        ]
        # sensordata["gyro"] = [(time_since_start*2)%60, time_since_start%90, time_since_start%90]
        # sensordata["time"] = [time_since_start]
        sensordata["thrust"] = [
            thrust_list[(0 + count) % 201],
            thrust_list[(13 + count) % 201],
            thrust_list[(25 + count) % 201],
            thrust_list[(38 + count) % 201],
            thrust_list[(37 + count) % 201],
            thrust_list[(50 + count) % 201],
            thrust_list[(63 + count) % 201],
            thrust_list[(75 + count) % 201],
            thrust_list[(88 + count) % 201],
            thrust_list[(107 + count) % 201],
        ]
        # sensordata["thrust"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        gui_pipe.send(sensordata)
        time.sleep(1)


class Rov_state:
    def __init__(self, queue, gui_pipe, t_watch: Threadwatcher) -> None:
        self.queue = multiprocessing.Queue = queue  # queue to rov
        self.gui_pipe = gui_pipe  # pipe to gui
        self.t_watch: Threadwatcher = t_watch  # threadwatcher to control threads
        self.sensordata = None
        self.time_since_packet_update = []
        self.send_sensordata_to_gui()
        self.main_loop

    def send_sensordata_to_gui(self, data):
        print(f"sending data from main to gui: {data =}")
        self.gui_pipe.send(data)


def send_fake_sensordata(t_watch: Threadwatcher, gui_pipe: multiprocessing.Pipe):
    thrust_list = [num for num in range(-100, 101)]
    power_list = [num for num in range(0, 101)]
    count = -1
    sensordata = {}
    while t_watch.should_run(0):
        # time_since_start = round(time.time()-start_time_sec)
        count += 1
        sensordata["lekk_temp"] = [
            True,
            True,
            True,
            (25 + count) % 60,
            (37 + count) % 60,
            (61 + count) % 60,
        ]
        sensordata["thrust"] = [
            thrust_list[(0 + count) % 201],
            thrust_list[(13 + count) % 201],
            thrust_list[(25 + count) % 201],
            thrust_list[(38 + count) % 201],
            thrust_list[(37 + count) % 201],
            thrust_list[(50 + count) % 201],
            thrust_list[(63 + count) % 201],
            thrust_list[(75 + count) % 201],
            thrust_list[(88 + count) % 201],
            thrust_list[(107 + count) % 201],
        ]
        sensordata["power_consumption"] = [
            power_list[count % 101] * 13,
            power_list[count % 101] * 2.4,
            power_list[count % 101] * 0.65,
        ]
        # TODO: sensordata["gyro"] = [(time_since_start*2)%60, time_since_start%90, time_since_start%90]
        # TODO: sensordata["time"] = [time_since_start]
        sensordata["thrust"] = [
            thrust_list[(0 + count) % 201],
            thrust_list[(13 + count) % 201],
            thrust_list[(25 + count) % 201],
            thrust_list[(38 + count) % 201],
            thrust_list[(37 + count) % 201],
            thrust_list[(50 + count) % 201],
            thrust_list[(63 + count) % 201],
            thrust_list[(75 + count) % 201],
            thrust_list[(88 + count) % 201],
            thrust_list[(107 + count) % 201],
        ]
        # sensordata["thrust"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        gui_pipe.send(sensordata)
        time.sleep(1)


# TODO: bruh what


def test_gui_leak_response(gui_pipe: multiprocessing.Pipe):
    sensordata = {"lekk_temp": [False, False, False, -1, -1, -1]}
    gui_pipe.send(sensordata)


if __name__ == "__main__":
    try:
        global time_since_start
        global start_time_sec
        global run_gui
        global manual_input_rotation
        global run_network
        global run_craft_packet
        start_time_sec = time.time()
        run_gui = True
        run_get_controllerdata = False
        run_network = False
        run_craft_packet = True
        run_send_fake_sensordata = True
        manual_input_rotation = False

        queue_for_rov = multiprocessing.Queue()

        t_watch = Threadwatcher()
        
        (
            gui_parent_pipe,#Used by main process, to send/receive data to gui
            gui_child_pipe,#Used by gui process, to send/receive data to main
        ) = Pipe()  # starts the gui program. gui_parent_pipe should get the sensor data
        
        if run_gui:
            id = t_watch.add_thread()
            gui_loop = Process(
                target=gui.run,
                args=(gui_child_pipe, queue_for_rov, t_watch, id),
                daemon=True,
            )  # and should recieve commands from the gui
            gui_loop.start()

        # TODO: add controller
        # if run_get_controllerdata:
        #    id = t_watch.add_thread()
        # takes in controller data and sends it into child_conn
        #    controller_process = Process(target=controller.run, args=(queue_for_rov, t_watch, id,True, False,), daemon=True)
        #    controller_process.start()

        # Network is blocking
        # network = None #TODO: add network
        # if run_network:
        #    network = Network(is_server=False, port=6900, connect_addr="10.0.0.2")
        #    print("network started")

        # TODO: add real data lol
        # print("starting send to rov")
        # id = t_watch.add_thread()
        # main_driver_loop = threading.Thread(target=run, args=(network, t_watch, id, queue_for_rov, gui_parent_pipe), daemon=True)
        # main_driver_loop.start()

        if run_send_fake_sensordata:
            id = t_watch.add_thread()
            datafaker = threading.Thread(
                target=send_fake_sensordata,
                args=(t_watch, gui_parent_pipe),
                daemon=True,
            )
            datafaker.start()

        test_gui_leak_response(gui_parent_pipe)

        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        gui_loop.kill()

        t_watch.stop_all_threads()
        print("stopped all threads")
