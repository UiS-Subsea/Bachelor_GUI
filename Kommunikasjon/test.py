
# def reset_12V_thruster_fuse(self, fuse_number):
#     self.regulator_active: list[bool] = [True, True, True]
#     packets_to_send = []

#     """reset_fuse_on_power_supply creates and adds
#     packets for resetting a fuse on the ROV"""
#     byte0 = 0b10000000 | (fuse_number << 1)
#     fuse_reset_signal = [byte0]

#     for item in self.regulator_active:
#         fuse_reset_signal.append(item)

#     self.packets_to_send.append([98, fuse_reset_signal])
#     print(packets_to_send)

# Test1
def set_zero_point_depth(sensordata=None):
    packets_to_send = []
    print("1")
    zero_point_packet = bytes([66, 0b10000000])
    print("2")
    print(zero_point_packet)
    packets_to_send.append([zero_point_packet, []])
    print("3")
    print(packets_to_send)

# Test2
def set_zero_point_depth2(sensordata=None):
    packets_to_send = []
    ID_RESET_DEPTH = 66
    BYTE0_INIT_FLAG = 0b00000010
    print(BYTE0_INIT_FLAG)
    packets_to_send.append([ID_RESET_DEPTH, [BYTE0_INIT_FLAG]])
    print(packets_to_send)
    print([ID_RESET_DEPTH, [BYTE0_INIT_FLAG]])


if __name__ == "__main__":
    s = set_zero_point_depth2()
    print(s)
