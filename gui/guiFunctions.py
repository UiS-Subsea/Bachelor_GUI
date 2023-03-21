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
def nullpunktDybde(window):
    print("Nullpunkt Dybde")

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



