import multiprocessing
import time
from Thread_info import Threadwatcher

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
    thrust_list = [num for num in range(-100, 101)]
    manipulator_list = [num for num in range(-100, 101)]
    power_list = [num for num in range(0, 101)]
    vinkel_list = [num for num in range(-360, 360)]
    dybde_list = [num for num in range(50, 20000)]

    # Errors
    imuErrors = [True, False, False, False, False, False, False, False]
    tempErrors = [False, True, False, False]
    pressureErrors = [True, False, True, False]
    leakageAlarms = [True, False, False, False]
    ManipulatorSikring = [False, False, True]
    ThrusterSikring = [False, True, False]
    KraftSikring = [False, False, True]

    count = -1
    sensordata = {}
    while t_watch.should_run(0):
        count += 1
        sensordata[VINKLER] = [
            dybde_list[(0 + count)],
            dybde_list[(10 + count)],
            dybde_list[(20 + count)],
            dybde_list[(30 + count)],
            dybde_list[(40 + count)],
            dybde_list[(50 + count)],
            dybde_list[(60 + count)],
        ]
        sensordata[DYBDETEMP] = [
            vinkel_list[(0 + count)],  # dybde
            vinkel_list[(12 + count)],  # vanntemp
            vinkel_list[(45 + count) % 201],  # sensorkorttemp
        ]

        sensordata[FEILKODE] = [
            imuErrors,
            tempErrors,
            pressureErrors,
            leakageAlarms,
        ]

        sensordata[THRUST] = [
            thrust_list[(0 + count) % 201],
            thrust_list[(13 + count) % 201],
            thrust_list[(25 + count) % 201],
            thrust_list[(38 + count) % 201],
            thrust_list[(37 + count) % 201],
            thrust_list[(50 + count) % 201],
            thrust_list[(63 + count) % 201],
            thrust_list[(75 + count) % 201],
            thrust_list[(88 + count) % 201],
        ]
        sensordata[MANIPULATOR12V] = [
            manipulator_list[(0 + count)],  # Strømtrekk
            manipulator_list[(5 + count)],  # Temperatur
            ManipulatorSikring,  # Sikringsstatus
        ]
        sensordata[THRUSTER12V] = [
            thrust_list[(0 + count)],  # Strømtrekk
            manipulator_list[(5 + count)],  # Temperatur
            ThrusterSikring,
        ]

        sensordata[KRAFT5V] = [
            power_list[count % 101] * 13,
            power_list[count % 101] * 2.4,
            KraftSikring,
        ]
        sensordata[REGULERINGMOTORTEMP] = [
            power_list[count % 101] * 13,
            power_list[count % 101] * 2.4,
        ]
        sensordata[TEMPKOMKONTROLLER] = [power_list[count % 101] * 13]

        gui_queue.put(sensordata)
        time.sleep(0.5)
