import multiprocessing
import time
from Thread_info import Threadwatcher
import random

MANIPULATOR_IN_OUT = 15
MANIPULATOR_ROTATION = 0
MANIPULATOR_TILT = 3
MANIPULATOR_GRAB_RELEASE = 6


REGULERINGSKNAPPAR = "32"  # 0=All regulering deaktivert, 1=Aktiver rull reg, 2=Regulering av dybde aktivert, 3=Regulering av vinkel aktivert, 4=Regulering av dybde og vinkel aktivert
THRUST = "129"  # HHF, #HHB, #HVB, HVF, VHF, VHB, VVB, VVF //GOOD
REGULERINGMOTORTEMP = "130"  # 0Reguleringskort, 1=Motordriverkort
VINKLER = "138"  # 0=roll, 1=stamp, 2=gir? //GOOD
DYBDETEMP = "139"  # 0=dybde, 2=vanntemp, 4=sensorkorttemp //GOOD
FEILKODE = "140"  # 0=IMU Error, 1=Temp Error, 2=Trykk Error, 3=Lekkasje //GOOD
TEMPKOMKONTROLLER = "145"  # =Temp
MANIPULATOR12V = "150"  # Strømtrekk, Temperatur, Sikringsstatus //GOOD
THRUSTER12V = "151"  # Strømtrekk, Temperatur, Sikringsstatus
KRAFT5V = "152"  # Strømtrekk, Temperatur, Sikringsstatus


VALIDCOMMANDS = [
    THRUST,
    REGULERINGMOTORTEMP,
    VINKLER,
    DYBDETEMP,
    FEILKODE,
    TEMPKOMKONTROLLER,
    MANIPULATOR12V,
    THRUSTER12V,
    KRAFT5V,
]

# ROV
X_AXIS = 1
Y_AXIS = 0
Z_AXIS = 6
ROTATION_AXIS = 2

FRONT_LIGHT_ID = 98
BOTTOM_LIGHT_ID = 99

front_light_intensity = 0
bottom_light_intensity = 0


ID_DIRECTIONCOMMAND_PARAMETERS = 71
ID_DIRECTIONCOMMAND = 70
ID_camera_tilt_upwards = 200
ID_camera_tilt_downwards = 201


def send_fake_sensordata(t_watch: Threadwatcher, gui_queue: multiprocessing.Queue):
    thrust_list = [num for num in range(0, 101)]
    power_list = [num for num in range(0, 7)]
    vinkel_list = [num for num in range(30, 71)]
    dybde_list = [num for num in range(0, 101)]
    temperature_list = [num for num in range(0, 70)]
    vinkel_list = [num for num in range(0, 360)]

    # Errors
    imuErrors = [False, False, True, True, False, False, False, False]
    tempErrors = [True, True, False, False]
    pressureErrors = [False, True, True, False]
    leakageAlarms = [False, True, True, False]
    ManipulatorSikring = [False, False, True]
    ThrusterSikring = [False, False, False]
    KraftSikring = [False, False, False]

    count = -1
    sensordata = {}
    while t_watch.should_run(0):
        count += 1
        sensordata[VINKLER] = [
            vinkel_list[(0 + count) % len(vinkel_list)],
            vinkel_list[(10 + count) % len(vinkel_list)],
            vinkel_list[(20 + count) % len(vinkel_list)],
        ]
        sensordata[DYBDETEMP] = [
            dybde_list[(2 + count) % len(dybde_list)],  # dybde
            temperature_list[(50 + count) % len(temperature_list)],  # vanntemp
            temperature_list[(30 + count) % len(temperature_list)],  # sensorkorttemp
        ]

        sensordata[FEILKODE] = [
            imuErrors,
            tempErrors,
            pressureErrors,
            leakageAlarms,
        ]

        sensordata[THRUST] = [
            thrust_list[(0 + count) % len(thrust_list)],
            thrust_list[(13 + count) % len(thrust_list)],
            thrust_list[(25 + count) % len(thrust_list)],
            thrust_list[(38 + count) % len(thrust_list)],
            thrust_list[(37 + count) % len(thrust_list)],
            thrust_list[(50 + count) % len(thrust_list)],
            thrust_list[(63 + count) % len(thrust_list)],
            thrust_list[(75 + count) % len(thrust_list)],
            thrust_list[(88 + count) % len(thrust_list)],
        ]
        sensordata[MANIPULATOR12V] = [
            power_list[(0 + count) % len(power_list)],  # Strømtrekk
            temperature_list[(40 * 100 + count) % len(temperature_list)],  # Temperatur
            ManipulatorSikring,  # Sikringsstatus
        ]
        sensordata[THRUSTER12V] = [
            power_list[(0 + count) % len(power_list)],  # Strømtrekk
            temperature_list[(50 * 100 + count) % len(temperature_list)],  # Temperatur
            ThrusterSikring,
        ]

        sensordata[KRAFT5V] = [
            power_list[count % len(power_list)] % len(power_list),
            temperature_list[count % len(temperature_list)],
            KraftSikring,
        ]
        sensordata[REGULERINGMOTORTEMP] = [
            temperature_list[count % len(temperature_list)],
            temperature_list[count % len(temperature_list)],
            dybde_list[count % len(dybde_list)],
        ]
        sensordata[TEMPKOMKONTROLLER] = random.randint(30, 60)

        gui_queue.put(sensordata)
        time.sleep(0.5)
