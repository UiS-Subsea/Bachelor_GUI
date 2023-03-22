import multiprocessing
from Thread_info import Threadwatcher

#Generere Testdata
def create_test_sensordata(delta, old_sensordata=None):
    #TODO: don't use this later its a test function
    sensordata = {}
    if old_sensordata is None:
        sensordata = {"dybde": -2500.0, "spenning": 48.0, "temp_rov": 26.0}
    else:
        #sensordata["tid"] = int(time.time()-start_time_sec)
        sensordata["dybde"] = old_sensordata["dybde"] + 10*delta
        sensordata["spenning"] = old_sensordata["spenning"] + 0.4*delta
        sensordata["temp_rov"] = old_sensordata["temp_rov"] + 0.3*delta
    return sensordata

#Kjøremoduser
def manuellKjoring(window):
    print("Manuell Kjøring aktivert")

def autonomDocking(window):
    print("autonom Docking aktivert")
    
def frogCount(window):
    print("Frog Count aktivert")

#Sikringer
def reset5V(window):
    print("Reset 5V sikring")

def resetThruster(window):
    print("Reset Thruster sikring")

def resetManipulator(window):
    print("Reset Manipulator sikring")

#IMU
def kalibrerIMU(window):
    print("Kalibrer IMU")

#Dybde
def nullpunktDybde(window, sensordata=None):
    listen = []
    ID_RESET_DEPTH = 66
    BYTE0_INIT_FLAG = 0b00000010
    print(BYTE0_INIT_FLAG)
    window.packets_to_send.append([ID_RESET_DEPTH, [BYTE0_INIT_FLAG]])
    print(window.packets_to_send)
    print([ID_RESET_DEPTH, [BYTE0_INIT_FLAG]])

#Vinkler
def nullpunktVinkler(window):
    print("Nullpunkt Vinkler")

#Kamera
def tiltUp(window):
    print("Tilt Kamera Opp")

def tiltDown(window):
    print("Tilt Kamera Ned")

def takePic(window):
    print("Ta Bilde")

def savePic(window):
    print("Lagre Bilde")


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

