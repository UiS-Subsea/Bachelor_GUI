import multiprocessing
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets, Qt, uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QCheckBox, QLabel, QMessageBox
from PyQt5.QtMultimedia import QSound, QSoundEffect, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import sys
import threading
#from main import Vinkeldata

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
        pipe_conn_only_rcv,
        queue_for_rov: multiprocessing.Queue,
        queue_for_cam: multiprocessing.Queue,
        t_watch: Threadwatcher,
        id: int,
        parent=None,
    ):
        self.packets_to_send = []
        super().__init__(parent)
        uic.loadUi("gui/window1.ui", self)
        self.connectFunctions()
        self.sound_timer = QTimer()
        self.sound_timer.timeout.connect(self.play_sound)

        regulering_status_wait_counter = 0
        self.lekkasje_varsel_is_running = False
        self.ID_RESET_DEPTH = 66
        # Queue and pipe
        self.queue: multiprocessing.Queue = (
            queue_for_rov
        )
        # pipe_conn_only_rcv is a pipe connection that only receives data
        self.pipe_conn_only_rcv = pipe_conn_only_rcv
        # Threadwatcher
        self.t_watch: Threadwatcher = t_watch  # t_watch is a threadwatcher object
        self.id = id  # id is an id that is used to identify the thread

        self.gir_verdier = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.receive = threading.Thread(
            target=self.receive_sensordata, daemon=True, args=(self.pipe_conn_only_rcv,)
        )
        self.receive.start()

        
        # Use queue_for_rov to use the common queue!!!!
        # queue for cam is only for testing, only receives data from camerafeed funcs
        self.cam = ExecutionClass(queue_for_cam)
        self.w = None  # SecondWindow() #

        # Buttons
    def show_new_window(self, checked):
        if self.w is None:
            self.w = SecondWindow(self)
            self.w.show()
        else:
            print("window already open")

    def connectFunctions(self):
        # window2
        self.showNewWindowButton.clicked.connect(self.show_new_window)

        # Kjøremodus
        self.btnManuell.clicked.connect(lambda: self.cam.manual())
        self.btnAutonom.clicked.connect(lambda: self.cam.send_data_test())
        self.btnFrogCount.clicked.connect(lambda: self.cam.transect())

        # Sikringer
        self.btnReset5V.clicked.connect(lambda: Rov_state.reset_5V_fuse2(self))
        self.btnResetThruster.clicked.connect(
            lambda: Rov_state.reset_12V_manipulator_fuse(self))
        self.btnResetManipulator.clicked.connect(
            lambda: Rov_state.reset_12V_thruster_fuse(self))

        self.btnResetThruster.clicked.connect(lambda: f.resetThruster(self))
        self.btnResetManipulator.clicked.connect(
            lambda: f.resetManipulator(self))

        # IMU
        self.btnKalibrerIMU.clicked.connect(lambda: f.kalibrerIMU(self))

        # Dybde
        self.btnNullpunktDybde.clicked.connect(lambda: f.nullpunktDybde(self))

        # Vinkler
        self.btnNullpunktVinkler.clicked.connect(
            lambda: f.nullpunktVinkler(self))

    def receive_sensordata(
        self, conn
    ):  # conn is a pipe connection that only receives data
        self.communicate = (
            Communicate()
        )  # Create a new instance of the class Communicate
        self.communicate.data_signal.connect(
            self.decide_gui_update
        )  # Connect the signal to the function that decides what to do with the sensordata
        while self.t_watch.should_run(
            self.id
        ):  # While the threadwatcher says that the thread should run
            print("Waiting for sensordata")
            data_is_ready = conn.recv()  # Wait for sensordata
            # if self.regulering_status_wait_counter > 0: #Wait for regulering_status to be sent
            #    self.regulering_status_wait_counter -= 1 #Decrease counter
            if data_is_ready:
                sensordata: dict = (
                    conn.recv()
                )  # "sensordata" is a dictionary with all the sensordata
                self.communicate.data_signal.emit(
                    sensordata
                )  # Emit sensordata to the gui
            else:
                time.sleep(0.15)  # Sleep for 0.15 seconds
        print("received")
        exit(0)

    # def send_data_to_main(self, data, id):
    #     if self.queue is not None:
    #         self.queue.put([id, data])
    #     else:
    #         raise TypeError("self.queue does not exist inside send_data_to_main")

    def gui_manipulator_state_update(self, sensordata):
        self.toggle_mani.setChecked(sensordata[0])

    def decide_gui_update(self, sensordata):
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

        }
        for key in sensordata.keys():
            if key in self.sensor_update_function:
                self.sensor_update_function[key](sensordata[key])

    def start_sound(self):
        # start the timer with a delay of 2 seconds
        self.sound_timer.start(2000)

    def stop_sound(self):
        self.sound_timer.stop()

    def play_sound(self):
        # Load the sound file
        sound_file = 'D:\Bachelor_GUI\siren2.wav'

        # Create a QMediaPlayer object and set the media content
        player = QMediaPlayer()
        player.setMedia(QMediaContent(QUrl.fromLocalFile(sound_file)))

        # Connect the player's mediaStatusChanged signal to a lambda function that
        # stops and deletes the player when the playback is finished
        player.mediaStatusChanged.connect(lambda status: player.deleteLater(
        ) if status == QMediaPlayer.EndOfMedia else None)

        # Play the sound
        player.play()

    def guiFeilKodeUpdate(self, sensordata):
        labelIMUAlarm: QLabel = self.labelIMUAlarm
        labelLekkasjeAlarm: QLabel = self.labelLekkasjeAlarm
        labelTempAlarm: QLabel = self.labelTempAlarm
        labelTrykkAlarm: QLabel = self.labelTrykkAlarm

        if sensordata[0] == 1:
            labelIMUAlarm.setText("ADVARSEL!")
            labelIMUAlarm.setStyleSheet("color: red")
        if sensordata[1] == 1:
            labelTrykkAlarm.setText("ADVARSEL!")
            labelTrykkAlarm.setStyleSheet("color: red")
        if sensordata[2] == 1:
            labelTempAlarm.setText("ADVARSEL!")
            labelTempAlarm.setStyleSheet("color: red")
        if sensordata[3] == 1:
            labelLekkasjeAlarm.setText("ADVARSEL!")
            labelLekkasjeAlarm.setStyleSheet("color: red")
            # self.play_sound()

    def dybdeTempUpdate(self, sensordata):
        labelDybde: QLabel = self.labelDybde
        labelTempVann: QLabel = self.labelTempVann
        labelTempVannMSB: QLabel = self.labelTempVannMSB
        labelTempSensorKort: QLabel = self.labelTempSensorkort
        labelTempSensorKortMSB: QLabel = self.labelTempSensorkortMSB
        labelSnittTemp: QLabel = self.labelSnittTemp

        labelDybde.setText(str(round(sensordata[0], 2)) + " m")

        labelTempVann.setText(str(round(sensordata[1], 2)) + " °C")
        if sensordata[1] > 50:
            labelTempVann.setStyleSheet("color: red")
        labelTempVannMSB.setText(str(round(sensordata[2], 2)) + " °C")
        labelTempSensorKort.setText(str(round(sensordata[3], 2)) + " °C")
        labelTempSensorKortMSB.setText(str(round(sensordata[4], 2)) + " °C")
        snittTemp = (sensordata[1]+sensordata[2]+sensordata[3]+sensordata[4])/4
        labelSnittTemp.setText(str(round(snittTemp, 2)) + " °C")

    def guiAccelUpdate(self, sensordata):
        label: QLabel = self.labelAccel
        label.setText(str(round(sensordata[0], 2)) + " m/s^2")

    def guiVinkelUpdate(self, sensordata):
        labelRull: QLabel = self.labelRull
        labelStamp: QLabel = self.labelStamp
        labelGir: QLabel = self.labelGir

        labelRull.setText(str(round(sensordata[0], 2)) + "°")
        labelStamp.setText(str(round(sensordata[2], 2)) + "°")
        labelGir.setText(str(round(sensordata[4], 2)) + "°")

    def gui_watt_update(self, sensordata):
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

    # TODO: fiks lekkasje varsel seinare


def run(conn, queue_for_rov,queue_for_cam, t_watch: Threadwatcher, id):
    # TODO: add suppress qt warnings?

    app = QtWidgets.QApplication(
        sys.argv
    )  # Create an instance of QtWidgets.QApplication

    # Create an instance of our class
    win = Window(conn, queue_for_rov, queue_for_cam, t_watch, id)
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
        self.btnTakePic.clicked.connect(lambda: f.takePic(self))
        self.btnSavePic.clicked.connect(lambda: f.savePic(self))


class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(dict)


if __name__ == "__main__":
    run()
