from send_recieve import Rov_state

ID_camera_upwards = 200
ID_camera_downwards = 201
packets_to_send = []


def hud_toggle(self, id):
    current_status = self.hud_status[id]

    new_status = not current_status
    self.hud_status[id] = new_status

    hud_dict = {"hud": new_status}

    packet_id = ID_camera_upwards + id
    packet_data = [packet_id, hud_dict]
    self.packets_to_send.append(packet_data)
