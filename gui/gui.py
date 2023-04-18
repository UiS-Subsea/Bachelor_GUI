import multiprocessing
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets, Qt, uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QCheckBox, QLabel, QMessageBox
from PyQt5.QtMultimedia import QSound, QSoundEffect, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer
import sys
import threading
#from main import Vinkeldata
from main import Rov_state
from . import guiFunctions as f
from Thread_info import Threadwatcher
import time
from camerafeed.GUI_Camerafeed_Main import *
import json
import multiprocessing
from Kommunikasjon.network_handler import Network
from multiprocessing import Process, Pipe
import threading
import time
from Kommunikasjon.packet_info import Logger
from Thread_info import Threadwatcher
from Controller import Controller_Handler as controller
from main import *


class Window(QMainWindow):
    def __init__(
        self,
        gui_queue: multiprocessing.Queue,
        queue_for_rov: multiprocessing.Queue,
        t_watch: Threadwatcher,
        id: int,
        parent=None,
    ):
        #        self.send_current_light_intensity()
        self.packets_to_send = []
        super().__init__(parent)
        uic.loadUi("gui/window1.ui", self)
        self.connectFunctions()
        self.player = QMediaPlayer()
        self.sound_file = "martinalarm.wav"
        self.queue: multiprocessing.Queue = (
            queue_for_rov
        )

        # pipe_conn_only_rcv is a pipe connection that only receives data
        self.gui_queue = gui_queue
        self.t_watch: Threadwatcher = t_watch  # t_watch is a threadwatcher object
        self.id = id  # id is an id that is used to identify the thread

        # self.receive = threading.Thread(
        #     target=self.receive_sensordata, daemon=True, args=(self.pipe_conn_only_rcv,)
        # )
        # self.receive.start()

        self.exec = ExecutionClass(queue_for_rov)
        self.camera = CameraClass()
        self.w = None  # SecondWindow()
        self.gir_verdier = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        self.timer = QTimer() # Create a timer
        self.timer.timeout.connect(self.update_gui_data) # Connect timer to update_gui_data
        self.timer.start(100) # Adjust the interval to your needs

        # Queue and pipe

    # Buttons
    
    def update_gui_data(self):
        while not self.gui_queue.empty():
            sensordata = self.gui_queue.get()
            self.decide_gui_update(sensordata)

    def show_new_window(self, checked):
        if self.w is None:
            self.w = SecondWindow(self)
            self.w.show()
        else:
            print("window already open")

    def connectFunctions(self):
        # window2
        self.showNewWindowButton.clicked.connect(lambda: self.exec.normal_camera())

        # Kjøremodus
        self.btnManuell.clicked.connect(lambda: self.exec.manual())
        self.btnAutonom.clicked.connect(lambda: self.exec.send_data_test())
        self.btnFrogCount.clicked.connect(lambda: self.exec.transect())

        # Kamera
        self.btnTakePic.clicked.connect(lambda: self.exec.save_image())
        self.btnRecord.clicked.connect(lambda: self.exec.record())

        # Lys
        # Lag 2 av og på knapper top&bottom

#        self.slider_lys_forward.valueChanged.connect(
#            Rov_state.set_front_light_dimming(intensity=10))

        # self.slider_lys_forward.valueChanged.connect(
        #    lambda: self.send_current_light_intensity)
        # self.slider_lys_down.valueChanged.connect(
        #    lambda: self.send_current_light_intensity)

#        self.toggle_frontlys.stateChanged.connect(lambda: Rov_state.current_ligth_intensity)
#        self.toggle_havbunnslys.stateChanged.connect(self.send_current_ligth_intensity)

        # Sikringer
        self.btnReset5V.clicked.connect(lambda: Rov_state.reset_5V_fuse2(self))
        self.btnResetThruster.clicked.connect(
            lambda: Rov_state.reset_12V_manipulator_fuse(self))
        self.btnResetManipulator.clicked.connect(
            lambda: Rov_state.reset_12V_thruster_fuse(self))
#
#        self.btnResetThruster.clicked.connect(lambda: f.resetThruster(self))
#        self.btnResetManipulator.clicked.connect(
#            lambda: f.resetManipulator(self))

        # IMU
        self.btnKalibrerIMU.clicked.connect(
            lambda: Rov_state.calibrate_IMU(self))

        # Dybde
        self.btnNullpunktDybde.clicked.connect(
            lambda: Rov_state.reset_depth(self))

        # Vinkler
        self.btnNullpunktVinkler.clicked.connect(
            lambda: Rov_state.reset_angles(self))

    # def receive_sensordata(
    #     self, conn
    # ):  # conn is a pipe connection that only receives data
    #     self.communicate = (
    #         Communicate()
    #     )  # Create a new instance of the class Communicate
    #     self.communicate.data_signal.connect(
    #         self.decideGuiUpdate
    #     )  # Connect the signal to the function that decides what to do with the sensordata
    #     while self.t_watch.should_run(
    #         self.id
    #     ):  # While the threadwatcher says that the thread should run
    #         #print("Waiting for sensordata")
    #         data_is_ready = conn.recv()  # Wait for sensordata
    #         if data_is_ready:
    #             sensordata: dict = (conn.recv())  # "sensordata" is a dictionary with all the sensordata
    #             self.communicate.data_signal.emit(sensordata)  # Emit sensordata to the gui
    #         else:
    #             time.sleep(0.15)  # Sleep for 0.15 seconds
    #     print("received")
    #     exit(0)
    
    

    # def receive_sensordata(
    #     self, conn
    # ):  # conn is a pipe connection that only receives data
    #     self.communicate = (
    #         Communicate()
        # )  # Create a new instance of the class Communicate
        # self.communicate.data_signal.connect(
        #     self.decide_gui_update
        # )  # Connect the signal to the function that decides what to do with the sensordata
        # while self.t_watch.should_run(
        #     self.id
        # ):  # While the threadwatcher says that the thread should run
        #     # print("Waiting for sensordata")
        #     data_is_ready = conn.get()  # Wait for sensordata
        #     # if self.regulering_status_wait_counter > 0: #Wait for regulering_status to be sent
        #     #    self.regulering_status_wait_counter -= 1 #Decrease counter
        #     if data_is_ready:
        #         sensordata: dict = (
        #             conn.recv()
        #         )  # "sensordata" is a dictionary with all the sensordata
        #         self.communicate.data_signal.emit(
        #             sensordata
        #         )  # Emit sensordata to the gui
        #     else:
        #         time.sleep(0.15)  # Sleep for 0.15 seconds
        # print("received")
        # exit(0)

    def gui_manipulator_state_update(self, sensordata):
        self.toggle_mani.setChecked(sensordata[0])

    def decide_gui_update(self, sensordata):
        # print("Deciding with this data: ", sensordata)
        self.sensor_update_function = {
            # "lekk_temp": self.gui_lekk_temp_update,
            # "thrust": self.gui_thrust_update,
            # "accel": self.guiAccelUpdate,
            # "gyro": self.gui_gyro_update,
            # "time": self.gui_time_update,
            # "manipulator": self.gui_manipulator_update,
            # "watt": self.gui_watt_update,
            # "manipulator_toggled": self.gui_manipulator_state_update,
            # "regulator_strom_status": self.regulator_strom_status,
            # "regulering_status": self.gui_regulering_state_update,
            # "settpunkt": self.print_data
            VINKLER: self.guiVinkelUpdate,
            DYBDETEMP: self.dybdeTempUpdate,
            FEILKODE: self.guiFeilKodeUpdate,
            # MANIPULATOR :self.manipulatorUpdate

        }
        for key in sensordata.keys():
            if key in self.sensor_update_function:
                self.sensor_update_function[key](sensordata[key])

    def play_sound(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            # If the player is still playing, wait until the playback is finished
            self.player.stateChanged.connect(self.on_player_state_changed)
        else:
            # Otherwise, start playing the new sound
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.sound_file)))
            self.player.play()

    # def send_current_light_intensity(self):
    #     front_light_is_on: bool = False
    #     if self.slider_lys_forward.checkState() != 0:
    #         front_light_is_on = True

    #     bottom_light_is_on: bool = False
    #     if self.slider_lys_down.checkState() != 0:
    #         bottom_light_is_on = True

    def on_player_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            # When the playback is finished, disconnect the signal and start playing the new sound
            self.player.stateChanged.disconnect(self.on_player_state_changed)
            self.player.setMedia(QMediaContent(
                QUrl.fromLocalFile(self.sound_file)))
            self.player.play()

    def guiFeilKodeUpdate(self, sensordata):
        imuErrors = [  # Feilkoder fra IMU
            "HAL_ERROR",
            "HAL_BUSY",
            "HAL_TIMEOUT",
            "INIT_ERROR",
            "WHO_AM_I_ERROR",
            "MEMS_ERROR",
            "MAG_WHO_AM_I_ERROR",
        ]

        tempErrors = [  # Feilkoder fra temperatur
            "HAL_ERROR",
            "HAL_BUSY",
            "HAL_TIMEOUT",
        ]

        trykkErrors = [  # Feilkoder fra trykk
            "HAL_ERROR",
            "HAL_BUSY",
            "HAL_TIMEOUT",
        ]

        lekkasjeErrors = [  # Feilkoder fra lekkasje
            "Probe_1",
            "Probe_2",
            "Probe_3",
            "Probe_4",
        ]

        # Henter alle labels
        labelIMUAlarm: QLabel = self.labelIMUAlarm
        labelLekkasjeAlarm: QLabel = self.labelLekkasjeAlarm
        labelTempAlarm: QLabel = self.labelTempAlarm
        labelTrykkAlarm: QLabel = self.labelTrykkAlarm
        gradient = (
            "background-color: #444444; color: #FF0000; border-radius: 10px;")

        #TODO: kanskje legge til ekstra oppdatering seinare
        IMUAlarm = ""
        # Sjekker om det er feil i sensordataene
        for i in range(len(sensordata[0])):
            if sensordata[0][i] == True:
                labelIMUAlarm.setText(imuErrors[i])
                labelIMUAlarm.setStyleSheet(gradient)
                
        for i in range(len(sensordata[1])):
            if sensordata[1][i] == True:
                labelTempAlarm.setText(tempErrors[i])
                labelTempAlarm.setStyleSheet(gradient)
                
        for i in range(len(sensordata[2])):
            if sensordata[2][i] == True:
                labelTrykkAlarm.setText(trykkErrors[i])
                labelTrykkAlarm.setStyleSheet(gradient)  
                
        for i in range(len(sensordata[3])):
            if sensordata[3][i] == True:
                labelLekkasjeAlarm.setText(lekkasjeErrors[i])
                labelLekkasjeAlarm.setStyleSheet(gradient)
                self.play_sound()


    def guiVinkelUpdate(self, sensordata):
        vinkel_liste: list[QLabel] = [
            self.labelRull,
            self.labelStamp,
            self.labelGir
        ]
        for i, label in enumerate(vinkel_liste):
            label.setText(str(round(sensordata[i]/1000, 2)) + "°")

    def guiVinkelUpdate(self, sensordata):
        vinkel_liste: list[QLabel] = [
            self.labelRull,
            self.labelStamp,
            self.labelGir
        ]
        for i, label in enumerate(vinkel_liste):
            label.setText(str(round(sensordata[i]/1000, 2)) + "°")

    def dybdeTempUpdate(self, sensordata):
        temp_liste: list[QLabel] = [
            self.labelDybde,
            self.labelTempVann,
            self.labelTempSensorkort
        ]
        for i, label in enumerate(temp_liste):
            label.setText(str(round(sensordata[i], 2)) + "°")
   
    def guiKraft(self, sensordata):
        effekt_liste: list[QLabel] = [
            self.labelEffektThrustere,
            self.labelEffektManipulator,
            self.labelEffektElektronikk,
        ]
        color_list = ["rgb(30, 33, 38);"] * 3
        if sensordata[0] > 1000:
            color_list[0] = "#ff0000"
        if sensordata[1] > 200:
            color_list[1] = "#ff0000"
        if sensordata[2] > 40:
            color_list[2] = "#ff0000"

        for index, label in enumerate(effekt_liste):
            label.setText(str(round(sensordata[index])) + " W")
            label.setStyleSheet(
                f"background-color: {color_list[index]}; border-radius: 5px; border: 1px solid rgb(30, 30, 30);"
            )

    def update_round_percent_visualizer(self, value, text_label):
        text_label.setText(str(value))
        # self.round_percent_visualizer.setValue(value)
        # self.round_percent_visualizer.setFormat(str(value) + "%")

    def gui_thrust_update(self, sensordata):
        # print(f"thrust update: {sensordata = }")  # Print sensordata
        for i in range(len(sensordata)):  # For each value in sensordata
            if sensordata[i] > 100:  # If the value is greater than 100
                sensordata[i] = 100  # Set the value to 100

        # Update the labels
        self.update_round_percent_visualizer(
            sensordata[0], self.thrust_label_1)
        self.update_round_percent_visualizer(
            sensordata[1], self.thrust_label_2)
        self.update_round_percent_visualizer(
            sensordata[2], self.thrust_label_3)
        self.update_round_percent_visualizer(
            sensordata[3], self.thrust_label_4)
        self.update_round_percent_visualizer(
            sensordata[4], self.thrust_label_5)
        self.update_round_percent_visualizer(
            sensordata[5], self.thrust_label_6)
        self.update_round_percent_visualizer(
            sensordata[6], self.thrust_label_7)
        self.update_round_percent_visualizer(
            sensordata[7], self.thrust_label_8)

    def gui_manipulator_update(self, sensordata):
        self.update_round_percent_visualizer(0, self.label_percentage_mani_1)
        self.update_round_percent_visualizer(0, self.label_percentage_mani_2)
        self.update_round_percent_visualizer(0, self.label_percentage_mani_3)
        if sensordata[3]:
            if sensordata[0] != 0:  # åpne/lukke manipulator
                self.update_round_percent_visualizer(
                    round(sensordata[0] * 0.35), self.label_percentage_mani_1
                )
            elif sensordata[2] != 0:  # rotere manipulator
                self.update_round_percent_visualizer(
                    round(sensordata[2] * 0.35), self.label_percentage_mani_2
                )
            elif sensordata[1] != 0:  # inn ut med manipulator1
                self.update_round_percent_visualizer(
                    round(sensordata[1] * 0.35), self.label_percentage_mani_3
                )


def run(conn, queue_for_rov, t_watch: Threadwatcher, id):

    app = QtWidgets.QApplication(
        sys.argv
    )  # Create an instance of QtWidgets.QApplication

    # Create an instance of our class
    win = Window(conn, queue_for_rov, t_watch, id)
    GLOBAL_STATE = False
    win.show()  # Show the form

    app.exec()
    # sys.exit(app.exec())


class SecondWindow(QWidget):
    def __init__(self, main_window, parent=None,):
        super().__init__()
        uic.loadUi("gui/window2.ui", self)
        self.label = QLabel("Camera Window")
        self.main_window = main_window
        self.connectFunctions()

    def closeEvent(self, event):
        self.main_window.w = None
        event.accept()

    def connectFunctions(self):
        # Kamera
        self.btnTiltUp.clicked.connect(lambda: f.tiltUp(self))
        self.btnTiltDown.clicked.connect(lambda: f.tiltDown(self))


class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(dict)


if __name__ == "__main__":
    run()
