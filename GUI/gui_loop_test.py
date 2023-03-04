from PyQt5 import QtWidgets, uic, QtCore, QtGui, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QGridLayout
import sys
import multiprocessing
import threading
import time
COMMAND_TO_ROV_ID = 3

class MyWindow(QMainWindow):
    def __init__(self,pipe_conn_only_rcv):#Everything that goes in the window goes into this function
        super(MyWindow, self).__init__() #Think about self as the window 
        uic.loadUi("GUI\SUBSEAGUI.ui", self)
        #self.queue : multiprocessing.Queue = queue
        self.pipe_conn_only_rcv = pipe_conn_only_rcv
        self.receive = threading.Thread(target=self.receive_sensordata, daemon=True, args=(self.pipe_conn_only_rcv,))
        self.receive.start()
        self.connectFunctions()
        self.gir_verdier = [0,0,0,0,0,0,0,0,0,0]
        self.run_count = 0
        self.lekkasje_varsel_is_running=False
        self.create_and_connect_controls()
    
    def connectFunctions(self):    
        #self.button1.clicked.connect(self.buttonClick)
        pass
    
    def update_gui(self,data):
        print(f"updating gui with data: {data = }")
        self.dybde.setText(str(round(data["dybde"],4)))
        self.tid.setText(str(data["tid"]))
        self.spenning.setText(str(round(data["spenning"],4)))
        self.label_temp_ROV_hovedkort.setText(str(round(data["temp_rov"],4)))
        self.print_data(data)

    def receive_sensordata(self,conn):
        self.communicate=Communicate()
        self.communicate.data_signal.connect(self.decide_gui_update)
        print("waiting_for_data")
        while True:
            data_is_ready = conn.poll()   # check if new data is available to be received from a connection
            if data_is_ready:
                sensordata: dict = conn.recv()   # receive data from a connection
                self.communicate.data_signal.emit(sensordata)   # emit a signal with the received data
            else:
                time.sleep(0.15)   # sleep for a short time if there is no new data to receive

    def decide_gui_update(self, sensordata):
        self.sensor_update_function = {
        "lekk_temp": self.gui_lekk_temp_update,
        "thrust" : self.gui_thrust_update,
        #"accel": self.gui_acceleration_update,
        #"gyro": self.gui_gyro_update,
        "time": self.gui_time_update,
        #"manipulator": self.gui_manipulator_update,
        "power_consumption": self.gui_watt_update,
        "manipulator_toggled": self.gui_manipulator_state_update,
        #"regulator_strom_status": self.regulator_strom_status,
        #"regulering_status": self.gui_regulering_state_update,
        "settpunkt": self.print_data
        }
        for key in sensordata.keys():
            if key in self.sensor_update_function:
                self.sensor_update_function[key](sensordata[key])
                print(f"updating {key} with {sensordata[key]}")
            
    def print_data(self, sensordata):
        print(sensordata)
    
    def update_round_percent_visualizer(self, value, text_label, round_frame):
        """This function will update the various circles with a progress bar around and percent in the middle"""
        blue = "rgba(85, 170, 255, 255)"
        red = "rgb(226, 47, 53)"
        progress = (100 - value) / 100.0
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)
        color = blue
        if value < 0:
            stop_1 = str(progress - 1)
            stop_2 = str(progress - 0.001 -1)
            color = red
        if value == 100:
            stop_1 = "1.000"
            stop_2 = "1.000"
        htmlText = f"""<p align="center"><span style=" font-size:9pt;">{value}
        </span><span style=" font-size:9pt; vertical-align:super;">%</span></p>"""
        text_label.setText(htmlText)
        styleSheet = """QFrame{ border-radius: 30px; background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(77, 77, 127, 100), stop:{STOP_2} {COLOR}); }"""
        styleSheet = styleSheet.replace("{STOP_1}", str(stop_1)).replace("{STOP_2}", str(stop_2)).replace("{COLOR}", color)
        round_frame.setStyleSheet(styleSheet)
        
    def gui_manipulator_state_update(self, sensordata):
        self.toggle_mani.setChecked(sensordata[0])
    def gui_thrust_update(self, sensordata):
    # print(f"ran gui_thrust_update {sensordata = }")
        for i in range(len(sensordata)):
            if sensordata[i] > 100:
                sensordata[i] = 100
        self.update_round_percent_visualizer(sensordata[0], self.label_percentage_HHF, self.frame_HHF)
        self.update_round_percent_visualizer(sensordata[1], self.label_percentage_HHB, self.frame_HHB)
        self.update_round_percent_visualizer(sensordata[2], self.label_percentage_HVB, self.frame_HVB)
        self.update_round_percent_visualizer(sensordata[3], self.label_percentage_HVF, self.frame_HVF)
        self.update_round_percent_visualizer(sensordata[4], self.label_percentage_VHF, self.frame_VHF)
        self.update_round_percent_visualizer(sensordata[5], self.label_percentage_VHB, self.frame_VHB)
        self.update_round_percent_visualizer(sensordata[6], self.label_percentage_VVB, self.frame_VVB)
        self.update_round_percent_visualizer(sensordata[7], self.label_percentage_VVF, self.frame_VVF)

    def gui_time_update(self, sensordata):
        tid = round(sensordata[0])
        hours = tid//3600
        tid -= hours*3600

        minutes = tid//60
        tid -= minutes*60
        seconds = tid

        tid_string = f"{'0'+str(hours) if len(str(hours)) == 1 else str(hours)}:{'0'+str(minutes) if len(str(minutes)) == 1 else str(minutes)}:{'0'+str(seconds) if len(str(seconds)) == 1 else str(seconds)}"

        self.label_tid.setText(tid_string)
    
    def gui_manipulator_update(self, sensordata):
        self.update_round_percent_visualizer(0, self.label_percentage_mani_1, self.frame_mani_1)
        self.update_round_percent_visualizer(0, self.label_percentage_mani_2, self.frame_mani_2)
        self.update_round_percent_visualizer(0, self.label_percentage_mani_3, self.frame_mani_3)
        if sensordata[3]:
            if sensordata[0] != 0: # åpne/lukke manipulator
                self.update_round_percent_visualizer(round(sensordata[0]*0.35), self.label_percentage_mani_1, self.frame_mani_1)
            elif sensordata[2] != 0: # rotere manipulator
                self.update_round_percent_visualizer(round(sensordata[2]*0.35), self.label_percentage_mani_2, self.frame_mani_2)
            elif sensordata[1] != 0: # inn ut med manipulator1
                self.update_round_percent_visualizer(round(sensordata[1]*0.35), self.label_percentage_mani_3, self.frame_mani_3)

    def gui_thrust_update(self, sensordata):
        # print(f"ran gui_thrust_update {sensordata = }")
        for i in range(len(sensordata)):
            if sensordata[i] > 100:
                sensordata[i] = 100
        self.update_round_percent_visualizer(sensordata[0], self.label_percentage_HHF, self.frame_HHF)
        self.update_round_percent_visualizer(sensordata[1], self.label_percentage_HHB, self.frame_HHB)
        self.update_round_percent_visualizer(sensordata[2], self.label_percentage_HVB, self.frame_HVB)
        self.update_round_percent_visualizer(sensordata[3], self.label_percentage_HVF, self.frame_HVF)
        self.update_round_percent_visualizer(sensordata[4], self.label_percentage_VHF, self.frame_VHF)
        self.update_round_percent_visualizer(sensordata[5], self.label_percentage_VHB, self.frame_VHB)
        self.update_round_percent_visualizer(sensordata[6], self.label_percentage_VVB, self.frame_VVB)
        self.update_round_percent_visualizer(sensordata[7], self.label_percentage_VVF, self.frame_VVF)

    def gui_lekk_temp_update(self, sensordata):
        # self.check_data_types(sensordata["lekk_temp"], (int, float, float, float))
        # print(f"ran gui_lekk_temp_update {sensordata = }")
        # print(f"{sensordata =}")
        temp_label_list:list[QLabel] = [self.label_temp_ROV_hovedkort, self.label_temp_ROV_kraftkort,
         self.label_temp_ROV_sensorkort, self.label_gjsnitt_temp_ROV]
        lekkasje_liste: list[bool] = [sensordata[0], sensordata[1], sensordata[2]]
        if not isinstance(lekkasje_liste[0], bool):
            raise TypeError(f"Lekkasje sensor 1 has wrong type. {type(lekkasje_liste[0]) = }, {lekkasje_liste[0]} ")
        average_temp =  round(sum((sensordata[3:6]))/3)
        sensordata.append(average_temp)
        for i in range(4):
            temp_label_list[i].setText(str(sensordata[i+3]))
        if sensordata[3] > 61: # Høyeste temp sett ved kjøring i bassenget på skolen | Hovedkort
            temp_label_list[i].setStyleSheet("background-color: #ff0000; border-radius: 5px; border: 1px solid rgb(30, 30, 30);")
        else:
            temp_label_list[i].setStyleSheet("background-color: rgb(30, 33, 38); border-radius: 5px; border: 1px solid rgb(30, 30, 30);")
        if sensordata[4] > 51: # Høyeste temp sett ved kjøring i bassenget på skolen | Kraftkort
            temp_label_list[i].setStyleSheet("background-color: #ff0000; border-radius: 5px; border: 1px solid rgb(30, 30, 30);")
        else:
            temp_label_list[i].setStyleSheet("background-color: rgb(30, 33, 38); border-radius: 5px; border: 1px solid rgb(30, 30, 30);")
        if sensordata[5] > 46: # Høyeste temp sett ved kjøring i bassenget på skolen | Sensorkort
            temp_label_list[i].setStyleSheet("background-color: #ff0000; border-radius: 5px; border: 1px solid rgb(30, 30, 30);")
        else:
            temp_label_list[i].setStyleSheet("background-color: rgb(30, 33, 38); border-radius: 5px; border: 1px solid rgb(30, 30, 30);")

        id_with_lekkasje = []
        for lekkasje_nr, is_lekkasje in enumerate(lekkasje_liste):
            if not is_lekkasje:
                id_with_lekkasje.append(lekkasje_nr+1)
        if not self.lekkasje_varsel_is_running and len(id_with_lekkasje)>0:
            self.lekkasje_varsel_is_running = True
            threading.Thread(target=lambda: self.lekkasje_varsel(id_with_lekkasje)).start()
                
                # self.update_round_percent_visualizer(sensordata[0], self.label_percentage_HHB, self.frame_HHB)
    def gui_watt_update(self, sensordata):
        effekt_liste: list[QLabel] = [self.label_effekt_thrustere, self.label_effekt_manipulator, self.label_effekt_elektronikk]
        color_list = ["rgb(30, 33, 38);"]*3
        if sensordata[0] > 1000:
            color_list[0] = "#ff0000"
        if sensordata[1] > 200:
            color_list[1] = "#ff0000"
        if sensordata[2] > 40:
            color_list[2] = "#ff0000"

        for index, label in enumerate(effekt_liste):
            label.setText(str(round(sensordata[index])) + " W")
            label.setStyleSheet(f"background-color: {color_list[index]}; border-radius: 5px; border: 1px solid rgb(30, 30, 30);")

        # self.label_effekt_manipulator_2.setText(str(round(sensordata[1])) + " W")
        # self.label_effekt_elektronikk_2.setText(str(round(sensordata[2])) +" W")
    
    def send_data_to_main(self, data, id):
        """Sends data to the main thread. Data is a dict with id and data"""
        if self.queue is not None:
            self.queue.put((id, data))
        else:
            raise TypeError("Queue is None")
        
    def send_command_to_rov(self, command):
        """Sends at command to the rov eg. turn on lights at 60% power"""
        self.send_data_to_main(command, COMMAND_TO_ROV_ID)
    
    def create_and_connect_controls(self):
        self.btn_avslutt_stitching.clicked.connect(self.stop_stich)
    
    def stop_stich(self):
        self.send_command_to_rov("[stop_stitching]")
        print("hei mr dominykas i think i am sending data now")
    
def window(conn):
    app = QApplication(sys.argv)
    win = MyWindow(conn)
    win.show()
    sys.exit(app.exec_())

    
class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(dict)

#def window(conn, queue_for_rov):
#    app = QApplication(sys.argv)
#    win = MyWindow(conn,queue_for_rov)
#    win.show()
#    sys.exit(app.exec_())

if __name__ == "__main__":
    #import SUBSEAGUI
    window()