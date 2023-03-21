
def reset_12V_thruster_fuse(self, fuse_number):
    self.regulator_active: list[bool] = [True, True, True]
    packets_to_send = []

    """reset_fuse_on_power_supply creates and adds
    packets for resetting a fuse on the ROV"""
    byte0 = 0b10000000 | (fuse_number << 1)
    fuse_reset_signal = [byte0]

    for item in self.regulator_active:
        fuse_reset_signal.append(item)

    self.packets_to_send.append([98, fuse_reset_signal])
    print(packets_to_send)    
