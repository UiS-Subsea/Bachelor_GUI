import multiprocessing
#from Thread_info import Threadwatcher
from main import *
# Kjøremoduser


def manuellKjoring(window):
    print("Manuell Kjøring aktivert")


def autonomDocking(window):
    print("autonom Docking aktivert")


def frogCount(window):
    print("Frog Count aktivert")

# Sikringer


def reset5V(window):
    Rov_state.reset_5V_fuse2()
    print("Reset 5V sikring")


def resetThruster(window):
    print("Reset Thruster sikring")


def resetManipulator(window):
    print("Reset Manipulator sikring")

# IMU


def kalibrerIMU(window):
    print("Kalibrer IMU")

# Dybde


def nullpunktDybde(window):
    print("Nullpunkt dybde")


# Vinkler
def nullpunktVinkler(window):
    print("Nullpunkt Vinkler")

# Kamera


def tiltUp(window):
    print("Tilt Kamera Opp")


def tiltDown(window):
    print("Tilt Kamera Ned")


def takePic(window):
    print("Ta Bilde")


def savePic(window):
    print("Lagre Bilde")


if __name__ == "__main__":
    print("guiFunctions")
    # Klasse = Rov_state
    # reset_5V = Klasse.reset_5V_fuse2
    # print(reset_5V)
