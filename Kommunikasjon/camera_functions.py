from Kommunikasjon.send_recieve import *

ID_camera_upwards = 200
ID_camera_downwards = 201
packets_to_send = []

def check_if_toggle_camera_on_or_off(self, id=None):
    if id is None:
        id = self.active_camera
    print("Setter til en active camera")
    self.camera_is_on[id] = not self.camera_is_on[id]
    self.packets_to_send.append(ID_camera_upwards+id, {"on": self.camera_is_on})

def hud_toggle(self, id):
    current_status = self.hud_status[id]

    new_status = not current_status
    self.hud_status[id] = new_status

    hud_dict = {"hud": new_status}

    packet_id = ID_camera_upwards + id
    packet_data = [packet_id, hud_dict]
    self.packets_to_send.append(packet_data)

def toggle_active_camera(self, button_index):
    if self.camera_toggle_wait_counter == 0:
        # Changes camera id between 0, 1, and 2
        self.active_camera = (self.active_camera + 1) % 3
        print(f"Changed active camera to {self.active_camera}")
        self.camera_toggle_wait_counter = 6