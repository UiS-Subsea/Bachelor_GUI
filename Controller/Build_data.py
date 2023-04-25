

# VALUES: (0-7) -> index i: [0,0,0,0,0,0,0,0]
# MANIPULATOR
MANIPULATOR_IN_OUT = 0
MANIPULATOR_ROTATION = 1
MANIPULATOR_TILT = 2
MANIPULATOR_GRAB_RELEASE = 7

# ROV
X_AXIS = 1
Y_AXIS = 0
Z_AXIS = 6
ROTATION_AXIS = 2


def build_manipulator_packet(self):
    data = [0, 0, 0, 0, 0, 0, 0, 0]
    # data = []
    data.append(self.data["mani_controller"][MANIPULATOR_IN_OUT])
    data.append(self.data["mani_controller"][MANIPULATOR_ROTATION])
    data.append(self.data["mani_controller"][MANIPULATOR_TILT])
    data.append(self.data["mani_controller"][MANIPULATOR_GRAB_RELEASE])
    # self.packets_to_send.append([41, data])
    print(data)
    return data

# KAN OGSÅ GJØRES SLIK VED Å LEGGE TIL I LISTEN:


def build_rov_packet(self):
    data = [0, 0, 0, 0, 0, 0, 0, 0]
    data[0] = self.data["rov_controller"][X_AXIS]
    data[1] = self.data["rov_controller"][Y_AXIS]
    data[2] = self.data["rov_controller"][Z_AXIS]
    data[3] = self.data["rov_controller"][ROTATION_AXIS]
    # self.packets_to_send.append([40, data])
    print(data)
    return data


def build_rov_packet_test():
    # MÅ hente inn dataen fra pack_controller_values eller noe slikt for å kunne klare videre
    rov_data = [0, 0, 0, 0, 0, 0, 0, 0]
    rov_data[0] = [X_AXIS]
    rov_data[1] = [Y_AXIS]
    rov_data[2] = [Z_AXIS]
    rov_data[3] = [ROTATION_AXIS]
    full_rov_data = [[33], rov_data]
    # self.packets_to_send.append([40, data])
    print(full_rov_data)
    return full_rov_data


def build_reset_packet(self):
    if self.data == {}:
        return
    data = [0, 0, 0, 0, 0, 0, 0, 0]

    data[0] = self.data["reset_controls"][0]

    self.packets_to_send.append([97, data])


def build_reset_thruster_packet(self):
    if self.data == {}:
        return
    data = [0, 0, 0, 0, 0, 0, 0, 0]

    data[0] = self.data["reset_controls_thruster"][0]

    self.packets_to_send.append([98, data])


def build_reset_manipulator_packet(self):
    if self.data == {}:
        return
    data = [0, 0, 0, 0, 0, 0, 0, 0]

    data[0] = self.data["reset_controls_manipulator"][0]

    self.packets_to_send.append([99, data])


def build_reset_depth(self):
    if self.data == {}:
        return
    data = [0, 0, 0, 0, 0, 0, 0, 0]

    data[0] = self.data["reset_depth"][0]

    self.packets_to_send.append([66, data])


def build_reset_angles(self):
    if self.data == {}:
        return
    data = [0, 0, 0, 0, 0, 0, 0, 0]

    data = self.data["reset_angles"]

    self.packets_to_send.append([66, data])


def build_calibrate_IMU(self):
    if self.data == {}:
        return
    data = [0, 0, 0, 0, 0, 0, 0, 0]

    data[2] = self.data["kalibrer_IMU"][2]

    self.packets_to_send.append([66, data])
