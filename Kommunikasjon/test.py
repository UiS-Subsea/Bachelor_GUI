
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


def reset_depth():
    packets_to_send = []
    angle_bit_state = 0

    reset_angles_byte = [0] * 8
    # toggle the bit
    if angle_bit_state == 0:
        reset_angles_byte[0] |= (1 << 0)
        angle_bit_state = 1
        print("Setting All Regulator To True")
        if reset_angles_byte[0] & (1 << 0):  # check if bit 0 is set to 1
            reset_angles_byte[0] |= (1 << 1)  # set bit 1 to 1
            reset_angles_byte[0] |= (1 << 2)  # set bit 2 to 1
            reset_angles_byte[0] |= (1 << 3)  # set bit 3 to 1
    elif angle_bit_state == 1:
        reset_angles_byte[0] |= (0 << 0)
        angle_bit_state = 0
        print("Setting All Regulators To False")
        if reset_angles_byte[0] & (0 << 0):
            reset_angles_byte[0] |= (0 << 1)  # set bit 1 to 1
            reset_angles_byte[0] |= (0 << 2)  # set bit 2 to 1
            reset_angles_byte[0] |= (0 << 3)  # set bit 3 to 1
    packets_to_send.append([32, bytes(reset_angles_byte)])
    print(packets_to_send)


if __name__ == "__main__":
    reset_depth()
#     s = set_zero_point_depth2()
#     print(s)
