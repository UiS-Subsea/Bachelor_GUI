
# # def reset_12V_thruster_fuse(self, fuse_number):
# #     self.regulator_active: list[bool] = [True, True, True]
# #     packets_to_send = []

# #     """reset_fuse_on_power_supply creates and adds
# #     packets for resetting a fuse on the ROV"""
# #     byte0 = 0b10000000 | (fuse_number << 1)
# #     fuse_reset_signal = [byte0]

# #     for item in self.regulator_active:
# #         fuse_reset_signal.append(item)

# #     self.packets_to_send.append([98, fuse_reset_signal])
# #     print(packets_to_send)

# # Test1
# def set_zero_point_depth(sensordata=None):
#     packets_to_send = []
#     print("1")
#     zero_point_packet = bytes([66, 0b10000000])
#     print("2")
#     print(zero_point_packet)
#     packets_to_send.append([zero_point_packet, []])
#     print("3")
#     print(packets_to_send)

# # Test2
# def set_zero_point_depth2(sensordata=None):
#     packets_to_send = []
#     ID_RESET_DEPTH = 66
#     BYTE0_INIT_FLAG = 0b00000010
#     print(BYTE0_INIT_FLAG)
#     packets_to_send.append([ID_RESET_DEPTH, [BYTE0_INIT_FLAG]])
#     print(packets_to_send)
#     print([ID_RESET_DEPTH, [BYTE0_INIT_FLAG]])


# if __name__ == "__main__":
#     s = set_zero_point_depth2()
#     print(s)

# regulator_active: list[bool] = [True, True, True]
# packets_to_send = []


# def reset_12V_thruster_fuse(fuse_number):
#     """reset_fuse_on_power_supply creates and adds
#     packets for resetting a fuse on the ROV"""
#     byte0 = 0b0000001
#     fuse_reset_signal = [byte0]
#     print(byte0)

#     # for item in regulator_active:    #Trenger vi denne for loopen?
#     #    fuse_reset_signal.append(item)

#     packets_to_send.append([98, fuse_reset_signal])
#     print(packets_to_send)

# if __name__ == "__main__":
#     r = reset_12V_thruster_fuse(1)
#     print(r)
# regulator_active: list[bool] = [True, True, True]
# packets_to_send = []
# X_AXIS = 1
# Y_AXIS = 0
# Z_AXIS = 6
# ROTATION_AXIS = 2
# data = {}


# def build_rov_packet():
#     data = [0, 0, 0, 0, 0, 0, 0, 0]
#     data[0] = data["rov_joysticks"][X_AXIS]
#     data[1] = data["rov_joysticks"][Y_AXIS]
#     data[2] = data["rov_joysticks"][Z_AXIS]
#     data[3] = data["rov_joysticks"][ROTATION_AXIS]
#     packets_to_send.append([40, data])
#     print(packets_to_send)
#     # print(self.packets_to_send)


# if __name__ == "__main__":
#     r = build_rov_packet()
#     print(r)


def reset_fuse_on_power_supply():
    """reset_fuse_on_power_supply creates and adds
    packets for resetting a fuse on the ROV"""
    packets_to_send = []
    fuse_reset_signal = [0] * 8
    fuse_reset_signal[0] = 1  # set bit 0 of byte 0 to 1 to turn on the fuse

    packets_to_send.append([66, fuse_reset_signal])
    print(packets_to_send)


if __name__ == "__main__":
    print(reset_fuse_on_power_supply())
