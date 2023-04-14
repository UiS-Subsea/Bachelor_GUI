
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


def reset_12V_manipulator_fuse():
    packets_to_send = []
    reset_fuse_byte = bytearray(8)  # Create byte array to represent 8 bytes
    reset_fuse_byte[0] |= 1
    # Clear other bits that might be used by other functions
    # reset_fuse_byte[0] &= ~(1 << 1)  # Clear bit 1
    # reset_fuse_byte[0] &= ~(1 << 2)  # Clear bit 2
    reset_fuse_byte[0] &= ~(1 << 3)  # Clear bit 3
    reset_fuse_byte[0] &= ~(1 << 4)  # Clear bit 4
    reset_fuse_byte[0] &= ~(1 << 5)  # Clear bit 5
    reset_fuse_byte[0] &= ~(1 << 6)  # Clear bit 6
    reset_fuse_byte[0] &= ~(1 << 7)  # Clear bit 7
    print("Resetting 12V Manipulator Fuse")
    packets_to_send.append((99, bytes(reset_fuse_byte)))
    print(packets_to_send)


if __name__ == "__main__":
    reset_12V_manipulator_fuse()
#     s = set_zero_point_depth2()
#     print(s)
