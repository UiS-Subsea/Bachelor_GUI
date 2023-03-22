

# VALUES: (0-7) -> index i: [0,0,0,0,0,0,0,0]
#MANIPULATOR
MANIPULATOR_IN_OUT = 0
MANIPULATOR_ROTATION = 1
MANIPULATOR_TILT = 2
MANIPULATOR_GRAB_RELEASE = 7

#ROV
X_AXIS = 1
Y_AXIS = 0
Z_AXIS = 6
ROTATION_AXIS = 2

def build_manipulator_packet(self):
    # data = [0,0,0,0,0,0,0,0]
    data = []
    data.append(self.data["mani_controller"][MANIPULATOR_IN_OUT])
    data.append(self.data["mani_controller"][MANIPULATOR_ROTATION])
    data.append(self.data["mani_controller"][MANIPULATOR_TILT])
    data.append(self.data["mani_controller"][MANIPULATOR_GRAB_RELEASE])
    self.packets_to_send.append([41, data])

#KAN OGSÅ GJØRES SLIK VED Å LEGGE TIL I LISTEN:
def build_rov_packet(self):
    data = []
    data[0] = self.data["rov_controller"][X_AXIS]
    data[1] = self.data["rov_controller"][Y_AXIS]
    data[2] = self.data["rov_controller"][Z_AXIS]
    data[3] = self.data["rov_controller"][ROTATION_AXIS]
    self.packets_to_send.append([40, data])