import multiprocessing
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets, Qt, uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QCheckBox, QLabel, QMessageBox
from PyQt5.QtMultimedia import QSound, QSoundEffect, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer, QObject, pyqtSignal
import os
import sys
import threading
from pyqtgraph import *
from RovState.send_fake_sensordata import REGULERINGMOTORTEMP
from images import resources_rc

# from main import Vinkeldata
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

global RUN_MANUAL
os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland.warning=false"


class Window(QMainWindow):
    def __init__(
        self,
        gui_queue: multiprocessing.Queue,
        queue_for_rov: multiprocessing.Queue,
        manual_flag,
        t_watch: Threadwatcher,
        id: int,
        parent=None,
    ):
        #        self.send_current_light_intensity()
        self.packets_to_send = []
        self.angle_bit_state = 0
        self.toggle_felles_regulator = [0] * 8


        super().__init__(parent)
        uic.loadUi("gui/mainwindow.ui", self)
        self.connectFunctions()
        self.player = QMediaPlayer()
        self.sound_file = "martinalarm.wav"
        self.sound_file = os.path.abspath("martinalarm.wav")

        self.sound_worker = SoundWorker(self.sound_file)
        self.sound_worker_thread = QThread()
        self.sound_worker.moveToThread(self.sound_worker_thread)
        self.sound_worker_thread.start()

        # Verdier for resetting av alarm
        self.lastBigAlarm = -1
        self.lastThrusterAlarm = -1
        self.lastManipulatorAlarm = -1
        self.lastIMUAlarm = -1
        self.lastTempAlarm = -1
        self.lastPressureAlarm = -1

        self.manual_flag = manual_flag
        # queue_for_rov is a queue that is used to send data to the rov
        self.queue = queue_for_rov
        # queue_for_rov is a queue that is used to send data to the rov

        self.gui_queue = gui_queue
        self.threadwatcher = t_watch
        self.id = id

        self.exec = ExecutionClass(queue_for_rov, manual_flag)
        self.camera = CameraClass()
        self.w = None  # SecondWindow()
        self.gir_verdier = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.timer = QTimer()  # Create a timer
        # Connect timer to update_gui_data
        self.timer.timeout.connect(self.update_gui_data)
        self.timer.start(100)  # Adjust the interval to your needs
        self.manual = True
        self.reguleringDropdown = self.findChild(QComboBox, "reguleringDropdown")
        self.tuningInput = self.findChild(QLineEdit, "tuningInput")
        self.btnRegTuning = self.findChild(QPushButton, "btnRegTuning")
        self.slider_lys_forward = self.findChild(QSlider, "slider_lys_forward")
        self.label_percentage_lys_forward = self.findChild(
            QLabel, "label_percentage_lys_forward"
        )
        self.slider_lys_down = self.findChild(QSlider, "slider_lys_down")
        self.label_percentage_lys_down = self.findChild(
            QLabel, "label_percentage_lys_down"
        )
        self.sliderCamVinkel = self.findChild(QSlider, "sliderCamVinkel")
        self.labelKameraVinkel = self.findChild(QLabel, "labelKameraVinkel")
        # self.sliderCamVinkel.setValue(90)

        # Queue and pipe

    # Buttons

    Gradient = "background-color: #444444; color: #FFFFFF; border-radius: 10px;"

    errorGradient = "background-color: #444444; color: #FF0000; border-radius: 10px;"

    def manual_kjoring(self):
        self.manual_flag.value = 1
        print("Manual flag: ", self.manual_flag.value)

        id = self.threadwatcher.add_thread()
        imageprocessing = threading.Thread(target=self.exec.stop_everything)
        imageprocessing.start()

    def imageprocessing(self, mode):
        self.manual_flag.value = 0
        print("Manual flag: ", self.manual_flag.value)
        if self.manual_flag.value == 0:
            if mode == "normal_camera":
                self.exec.send_data_test()
            if mode == "transect":
                self.exec.transect()
            if mode == "docking":
                self.exec.docking()
            if mode == "testing":
                self.exec.send_data_test()
        else:
            self.exec.stop_everything()

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
        self.showNewWindowButton.clicked.connect(
            lambda: self.imageprocessing("testing")
        )

        # Kjøremodus
        self.btnManuell.clicked.connect(lambda: self.manual_kjoring())
        self.btnAutonom.clicked.connect(lambda: self.imageprocessing("docking"))
        self.btnFrogCount.clicked.connect(lambda: self.imageprocessing("transect"))

        # Kamera
        self.btnTakePic.clicked.connect(lambda: self.exec.save_image())
        self.btnRecord.clicked.connect(lambda: self.exec.record())
        self.btnOpenCamera.clicked.connect(
            lambda: self.imageprocessing("normal_camera")
        )

        # Lys
        self.slider_lys_forward.valueChanged.connect(self.update_label_and_print_value)
        self.slider_lys_down.valueChanged.connect(
            self.update_label_and_print_value_down
        )
        self.sliderCamVinkel.valueChanged.connect(self.camVinkelUpdate)

        # Lag 2 av og på knapper top&bottom

        #        self.slider_lys_forward.valueChanged.connect(
        #            Rov_state.set_front_light_dimming(intensity=10))

        # self.slider_lys_forward.valueChanged.connect(
        #    lambda: self.send_current_light_intensity)
        # self.slider_lys_down.valueChanged.connect(
        #    lambda: self.send_current_light_intensity)

        self.btnTopLys.clicked.connect(lambda: self.front_light_on())
        self.btnBunnLys.clicked.connect(lambda: self.bottom_light_on())

        # Sikringer
        # self.btnReset5V.clicked.connect(lambda: self.reset_5V_fuse2())
        self.btnResetThruster.clicked.connect(lambda: self.reset_12V_thruster_fuse())
        self.btnResetManipulator.clicked.connect(
            lambda: self.reset_12V_manipulator_fuse()
        )
        #
        #        self.btnResetThruster.clicked.connect(lambda: f.resetThruster(self))
        #        self.btnResetManipulator.clicked.connect(
        #            lambda: f.resetManipulator(self))

        # IMU
        self.btnKalibrerIMU.clicked.connect(lambda: self.calibrate_IMU())

        # Dybde
        self.btnNullpunktDybde.clicked.connect(lambda: self.reset_depth())

        # Vinkler
        self.btnNullpunktVinkler.clicked.connect(lambda: self.reset_angles())

        self.btnRegTuning.clicked.connect(lambda: self.updateRegulatorTuning())

        # Regulatorer

        self.btnRegOn.clicked.connect(lambda: self.toogle_regulator_all())
        self.btnRullOn.clicked.connect(lambda: self.toggle_rull_reg())
        self.btnStampOn.clicked.connect(lambda: self.toggle_stamp_reg())
        self.btnDybdeOn.clicked.connect(lambda: self.toggle_dybde_reg())

    def gui_manipulator_state_update(self, sensordata):
        self.toggle_mani.setChecked(sensordata[0])

    def reset_5V_fuse2(self):
        """reset_5V_fuse creates and adds
        packets for resetting a fuse on the ROV"""
        reset_fuse_byte = [0] * 8
        reset_fuse_byte[0] |= 1 << 0  # reset bit 0
        print("Resetting 5V Fuse")
        values = {"reset_controls": reset_fuse_byte}
        print(("Want to send", 97, reset_fuse_byte))
        self.queue.put((4, values))

    def reset_12V_thruster_fuse(self):
        """reset_12V_thruster_fuse creates and adds
        packets for resetting a fuse on the ROV"""
        reset_fuse_byte = [0] * 8
        reset_fuse_byte[0] |= 1 << 0  # reset bit 0
        print("Resetting 12V Thruster Fuse")
        values = {"reset_controls_thruster": reset_fuse_byte}
        print(("Want to send", 98, reset_fuse_byte))
        self.queue.put((5, values))
        # reset_fuse_byte[0] |= (0 << 0)
        # print(f"Pakker Etter:", reset_fuse_byte)

    #        self.packets_to_send.append([98, reset_fuse_byte])

    def reset_12V_manipulator_fuse(self):
        """reset_12V_manipulator_fuse creates and adds
        packets for resetting a fuse on the ROV"""
        reset_fuse_byte = [0] * 8
        reset_fuse_byte[0] |= 1 << 0  # reset bit 0
        print("Resetting 12V Manipulator Fuse")
        values = {"reset_controls_manipulator": reset_fuse_byte}
        print(("Want to send", 99, reset_fuse_byte))
        self.queue.put((6, values))
        # reset_fuse_byte[0] |= (0 << 0)
        # print(f"Pakker Etter:", reset_fuse_byte)

        # self.packets_to_send.append([99, reset_fuse_byte])

    def reset_depth(self):
        reset_depth_byte = [0] * 8
        reset_depth_byte[0] |= 1 << 0  # reset bit 0
        print("Resetting Depth")
        values = {"reset_depth": reset_depth_byte}
        self.queue.put((7, values))
        print(("Want to send", 66, reset_depth_byte))
        # self.packets_to_send.append([66, reset_depth_byte])

    def reset_angles(self):
        reset_angles_byte = [0] * 8
        reset_angles_byte[0] |= 1 << 1  # reset bit 1
        print("Resetting Angles")
        values = {"reset_angles": reset_angles_byte}
        print(("Want to send", 66, reset_angles_byte))
        self.queue.put((8, values))
        # self.packets_to_send.append([66, reset_angles_byte])
        # print(reset_angles_byte)

    def calibrate_IMU(self):
        calibrate_IMU_byte = [0] * 8
        calibrate_IMU_byte[0] |= 1 << 2  # reset bit 2
        print("Kalibrerer IMU")
        values = {"kalibrer_IMU": calibrate_IMU_byte}
        print(("Want to send", 66, calibrate_IMU_byte))
        self.queue.put((9, values))
        # self.packets_to_send.append([66, calibrate_IMU_byte])
        # print(calibrate_IMU_byte)

    def update_label_and_print_value(self, value):
        self.label_percentage_lys_forward.setText(f"{value}%")
        set_light_byte = [0] * 8
        set_light_byte[1] = value
        values = {"slider_top_light": set_light_byte}
        print((f"Want to send", 98, set_light_byte))
        self.queue.put((17, values))
        print("Slider value:", value)

    def update_label_and_print_value_down(self, value):
        self.label_percentage_lys_down.setText(f"{value}%")
        set_light_byte = [0] * 8
        set_light_byte[1] = value
        values = {"slider_bottom_light": set_light_byte}
        print((f"Want to send", 99, set_light_byte))
        self.queue.put((18, values))
        print(value)

    def updateRegulatorTuning(self):
        reguleringDropdown = self.reguleringDropdown.currentText()
        input_value = float(self.tuningInput.text())

        my_dict = {
            "Rull KI": 1,
            "Rull KD": 2,
            "Rull KP": 3,
            "Stamp KI": 4,
            "Stamp KD": 5,
            "Stamp KP": 6,
            "Dybde KI": 7,
            "Dybde KD": 8,
            "Dybde KP": 9,
            "TS": 10,
            "Alpha": 11,
        }

        # None is default if key doesn't exist
        value = my_dict.get(reguleringDropdown, None)
        update_regulator_tuning = [int(value), float(input_value)]
        print(("Want to send", 42, update_regulator_tuning))
        #        self.packets_to_send.append([42, [int(value), float(input_value)]])
        values = {"update_regulator_tuning": update_regulator_tuning}
        self.queue.put((10, values))
        # print(("Want to send", 42, update_regulator_tuning))

    def toogle_regulator_all(self):
        self.angle_bit_state == 0
        toogle_regulator_byte = [0] * 8
        # toggle the bit
        if self.angle_bit_state == 0:
            toogle_regulator_byte[0] |= 1 << 0
            self.angle_bit_state = 1
            print("Setting All Regulator To True")
            # check if bit 0 is set to 1
            if toogle_regulator_byte[0] & (1 << 0):
                toogle_regulator_byte[0] |= 1 << 1  # set bit 1 to 1
                toogle_regulator_byte[0] |= 1 << 2  # set bit 2 to 1
                toogle_regulator_byte[0] |= 1 << 3  # set bit 3 to 1
        elif self.angle_bit_state == 1:
            toogle_regulator_byte[0] |= 0 << 0
            self.angle_bit_state = 0
            print("Setting All Regulators To False")
            if toogle_regulator_byte[0] & (0 << 0):
                toogle_regulator_byte[0] |= 0 << 1  # set bit 1 to 1
                toogle_regulator_byte[0] |= 0 << 2  # set bit 2 to 1
                toogle_regulator_byte[0] |= 0 << 3  # set bit 3 to 1
        print("Want to send", 32, toogle_regulator_byte)
        values = {"toggle_regulator_all": toogle_regulator_byte}
        self.queue.put((11, values))

    #        self.packets_to_send.append([32, toogle_regulator_byte])
    #        print(self.packets_to_send)

    def toggle_rull_reg(self):
        self.toggle_felles_regulator[0] ^= (1 << 0)
        if self.toggle_felles_regulator[0] == (1 << 0):
            print("rull på")
        elif self.toggle_felles_regulator[0] == (0 << 0):
            print("rull av")
        print(("Want to send", 32, self.toggle_felles_regulator))
        values = {"toggle_rull_reg": self.toggle_felles_regulator}
        self.queue.put((12, values))
        # if self.angle_bit_state == 0:
        #     self.toggle_felles_regulator[0] |= (1 << 0)
        #     self.angle_bit_state = 1
        #     print("Rull på")
        # elif self.angle_bit_state == 1:
        #     self.toggle_felles_regulator[0] |= (0 << 0)
        #     self.angle_bit_state == 0
        #     print("Rull av")
        # print(("Want to send", 32, self.toggle_felles_regulator))
        # values = {"toggle_rull_reg": self.toggle_felles_regulator}
        # self.queue.put((12, values))

    #        self.packets_to_send.append([66, toggle_rull_reg])

    def toggle_stamp_reg(self):
        self.toggle_felles_regulator[0] ^= (1 << 2)
        if self.toggle_felles_regulator[0] == (1 << 2):
            print("stamp på")
        elif self.toggle_felles_regulator[0] == (0 << 2):
            print("stamp av")
        print(("Want to send", 32, self.toggle_felles_regulator))
        values = {"toggle_rull_reg": self.toggle_felles_regulator}
        self.queue.put((12, values))


    def toggle_dybde_reg(self):
        self.toggle_felles_regulator[0] ^= (1 << 3)
        if self.toggle_felles_regulator[0] == (1 << 3):
            print("dybde på")
        elif self.toggle_felles_regulator[0] == (0 << 3):
            print("dybde av")
        print(("Want to send", 32, self.toggle_felles_regulator))
        values = {"toggle_rull_reg": self.toggle_felles_regulator}
        self.queue.put((12, values))


    def front_light_on(self):
        set_light_byte = [0] * 8
        set_light_byte[0] |= 1 << 1  # bit 1 to 1
        print("Front Light On")
        print(("Want to send", 98, set_light_byte))
        values = {"front_light_on": set_light_byte}
        self.queue.put((15, values))


    def bottom_light_on(self):
        set_light_byte = [0] * 8
        set_light_byte[0] |= 1 << 1  # bit 1 to 1
        print("Bottom Light On")
        print(("Want to send", 99, set_light_byte))
        values = {"bottom_light_on": set_light_byte}
        self.queue.put((16, values))



    # TODO: Spør dominykas om alt e rett :)
    def camVinkelUpdate(self, value):
        self.labelKameraVinkel.setText(f"{value}°")
        # set_light_byte = [0] * 8
        # set_light_byte[1] = value
        values = {"tilt": value}
        # print((f"Want to send", 200, values))
        self.queue.put((19, values))

        # self.queue.put((200,values))
        # print("SliderCamVinkel value:", value)

    def decide_gui_update(self, sensordata):
        # print("Deciding with this data: ", sensordata)
        self.sensor_update_function = {
            VINKLER: self.guiVinkelUpdate,
            DYBDETEMP: self.dybdeTempUpdate,
            FEILKODE: self.guiFeilKodeUpdate,
            THRUST: self.guiThrustUpdate,
            MANIPULATOR12V: self.guiManipulatorUpdate,
            THRUSTER12V: self.thruster12VUpdate,
            KRAFT5V: self.kraft5VUpdate,
            REGULERINGMOTORTEMP: self.reguleringMotorTempUpdate,
            TEMPKOMKONTROLLER: self.TempKomKontrollerUpdate,
        }
        for key in sensordata.keys():
            if key in self.sensor_update_function:
                self.sensor_update_function[key](sensordata[key])

    # def play_sound(self, should_play: bool):
    #     if should_play:
    #         if self.player.state() == QMediaPlayer.PlayingState:
    #             # If the player is still playing, wait until the playback is finished
    #             self.player.stateChanged.connect(self.on_player_state_changed)
    #         else:
    #             # Otherwise, start playing the new sound
    #             self.player.setMedia(QMediaContent(
    #                 QUrl.fromLocalFile(self.sound_file)))
    #             self.player.play()
    #     else:
    #         self.player.stop()

    # def send_current_light_intensity(self):
    #     front_light_is_on: bool = False
    #     if self.slider_lys_forward.checkState() != 0:
    #         front_light_is_on = True

    #     bottom_light_is_on: bool = False
    #     if self.slider_lys_down.checkState() != 0:
    #         bottom_light_is_on = True

    def play_sound(self, should_play: bool):
        self.sound_worker.play.emit(should_play)

    def closeEvent(self, event):
        self.sound_worker_thread.quit()
        self.sound_worker_thread.wait()

    def on_player_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.player.stateChanged.disconnect(self.on_player_state_changed)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.sound_file)))
            self.player.play()

    # def on_player_state_changed(self, state):
    #     if state == QMediaPlayer.StoppedState:
    #         # When the playback is finished, disconnect the signal and start playing the new sound
    #         self.player.stateChanged.disconnect(self.on_player_state_changed)
    #         self.player.setMedia(QMediaContent(
    #             QUrl.fromLocalFile(self.sound_file)))
    #         self.player.play()

    def guiFeilKodeUpdate(self, sensordata):
        imuErrors = [  # Feilkoder fra IMU
            "HAL_ERROR",
            "HAL_BUSY",
            "HAL_TIMEOUT",
            "INIT_ERROR",
            "WHO_AM_I_ERROR",
            "MEMS_ERROR",
            "MAG_WHO_AM_I_ERROerR",
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

        # TODO: kanskje legge til ekstra oppdatering seinare
        # Sjekker om det er feil i sensordataene
        for i in range(len(sensordata[0])):
            if sensordata[0][i] == True:
                labelIMUAlarm.setText(imuErrors[i])
                labelIMUAlarm.setStyleSheet(self.errorGradient)
                self.lastIMUAlarm = i

            if sensordata[0][i] == False and i == self.lastIMUAlarm:
                labelIMUAlarm.setText("Ingen feil")
                self.lastIMUAlarm = -1

        for i in range(len(sensordata[1])):
            if sensordata[1][i] == True:
                labelTempAlarm.setText(tempErrors[i])
                labelTempAlarm.setStyleSheet(self.errorGradient)
                self.lastTempAlarm = i

            if sensordata[1][i] == False and i == self.lastTempAlarm:
                labelIMUAlarm.setText("Ingen feil")
                self.lastTempAlarm = -1

        for i in range(len(sensordata[2])):
            if sensordata[2][i] == True:
                labelTrykkAlarm.setText(trykkErrors[i])
                labelTrykkAlarm.setStyleSheet(self.errorGradient)
                self.lastIMUAlarm = i

            if sensordata[2][i] == False and i == self.lastIMUAlarm:
                labelIMUAlarm.setText("Ingen feil")
                self.lastIMUAlarm = -1

        # TODO: skru på før du pusha
        for i in range(len(sensordata[3])):
            if sensordata[3][i] == True:
                labelLekkasjeAlarm.setText(lekkasjeErrors[i])
                labelLekkasjeAlarm.setStyleSheet(self.errorGradient)
                self.play_sound(True)
                self.lastBigAlarm = i
            if sensordata[3][i] == False and i == self.lastBigAlarm:
                labelLekkasjeAlarm.setText("Ingen feil")
                self.play_sound(False)
                self.lastBigAlarm = -1

    def guiVinkelUpdate(self, sensordata):
        vinkel_liste: list[QLabel] = [self.labelRull, self.labelStamp, self.labelGir]
        for i, label in enumerate(vinkel_liste):
            label.setText(str(round(sensordata[i] / 100, 2)) + "°")

    def dybdeTempUpdate(self, sensordata):
        labelDybde: QLabel = self.labelDybde

        # labelVann: QLabel = self.labelTempVann
        labelSensor: QLabel = self.labelTempSensorkort

        labelDybde.setText(str(round(sensordata[0], 2)) + "m")
        # labelVann.setText(str(round(sensordata[1], 2)) + "°C")
        labelSensor.setText(str(round(sensordata[2] / 100, 2)) + "°C")

    def guiThrustUpdate(self, sensordata):


        thrust_liste: list[QLabel] = [
            self.labelHHF,
            self.labelHHB,
            self.labelHVB,
            self.labelHVF,
            self.labelVHF,
            self.labelVHB,
            self.labelVVB,
            self.labelVVF,
        ]
        for i, label in enumerate(thrust_liste):
            label.setText(str(round(sensordata[i], 2)))

    kraftFeilkoder = [
        "Overcurrent trip",
        "Fuse fault",
        "Overtemp fuse",
    ]

    def guiManipulatorUpdate(self, sensordata):
        labelKraft: QLabel = self.labelManipulatorKraft
        labelTemp: QLabel = self.labelManipulatorTemp
        labelSikring: QLabel = self.labelManipulatorSikring

        labelKraft.setText(str(round(sensordata[0] / 1000, 2)) + "A")
        labelTemp.setText(str(round(sensordata[1] / 100, 2)) + "C")

        for i in range(3):
            if sensordata[2][i] == True:
                labelSikring.setText(str(self.kraftFeilkoder[i]))
                labelSikring.setStyleSheet(self.errorGradient)
                self.lastManipulatorAlarm = i

            if sensordata[2][i] == False and i == self.lastManipulatorAlarm:
                labelSikring.setText("Ingen feil")
                self.lastManipulatorAlarm = -1

    def thruster12VUpdate(self, sensordata):
        labelKraft: QLabel = self.labelThrusterKraft
        labelTemp: QLabel = self.labelThruster12VTemp
        labelSikring: QLabel = self.labelThrusterSikring
        # print(sensordata)

        labelKraft.setText(str(round(sensordata[0] / 1000, 2)) + "A")
        labelTemp.setText(str(round(sensordata[1] / 100, 2)) + "C")

        for i in range(3):
            if sensordata[2][i] == True:
                labelSikring.setText(str(self.kraftFeilkoder[i]))
                labelSikring.setStyleSheet(self.errorGradient)
                self.lastThrusterAlarm = i
            if sensordata[2][i] == False and i == self.lastThrusterAlarm:
                labelSikring.setText("Ingen feil")
                self.lastThrusterAlarm = -1

    def kraft5VUpdate(self, sensordata):
        labelTemp: QLabel = self.labelKraft5VTemp
        labelTemp.setText(str(round(sensordata[1] / 100, 2)) + "C")

    def reguleringMotorTempUpdate(self, sensordata):
        labelRegulering: QLabel = self.labelReguleringTemp
        labelMotor: QLabel = self.labelMotorTemp

        labelRegulering.setText(str(round(sensordata[0] / 100, 2)) + "°C")
        labelMotor.setText(str(round(sensordata[1] / 100, 2)) + "°C")
        print([130, sensordata[2]])


    def TempKomKontrollerUpdate(self, sensordata):
        labelTemp: QLabel = self.labelTempKomKontroller
        labelTemp.setText(str(round(sensordata, 2)) + "°C")


def run(conn, queue_for_rov, manual_flag, t_watch: Threadwatcher, id):
    app = QtWidgets.QApplication(
        sys.argv
    )  # Create an instance of QtWidgets.QApplication

    # Create an instance of our class
    win = Window(conn, queue_for_rov, manual_flag, t_watch, id)
    GLOBAL_STATE = False
    win.show()  # Show the form

    app.exec()
    # sys.exit(app.exec())


class SecondWindow(QWidget):
    def __init__(
        self,
        main_window,
        parent=None,
    ):
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


# A class for playing sound in a separate thread
class SoundWorker(QObject):
    play = pyqtSignal(bool)

    def __init__(self, sound_file):
        super().__init__()
        self.player = QMediaPlayer()
        self.sound_file = sound_file

        self.play.connect(self.on_play)

    def on_play(self, should_play: bool):
        if should_play:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stateChanged.connect(self.on_player_state_changed)
            else:
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.sound_file)))
                self.player.play()
        else:
            self.player.stop()

    def on_player_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.player.stateChanged.disconnect(self.on_player_state_changed)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.sound_file)))
            self.player.play()


# A class for communication between threads
class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(dict)


if __name__ == "__main__":
    run()
