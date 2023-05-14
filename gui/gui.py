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
        self.packets_to_send = []
        self.angle_bit_state = 0
        self.toggle_felles_regulator = [0] * 8

        super().__init__(parent)
        uic.loadUi("gui/mainwindow.ui", self)
        self.connectFunctions()

        # Sound
        self.player = QMediaPlayer()
        self.lydFil = "martinalarm.wav"
        self.lydFil = os.path.abspath("martinalarm.wav")
        self.sound_worker = SoundWorker(self.lydFil)
        self.sound_worker_thread = QThread()
        self.sound_worker.moveToThread(self.sound_worker_thread)
        self.sound_worker_thread.start()

        # Alarm managers
        self.currentManipulatorAlarms = set()
        self.currentThrusterAlarms = set()
        self.currentIMUAlarms = set()
        self.currentTempAlarms = set()
        self.currentTrykkAlarms = set()
        self.currentLekkasjeAlarms = set()

        # For going back to manual driving
        self.manual_flag = manual_flag

        self.queue = queue_for_rov  # Sending data
        self.gui_queue = gui_queue  # Receiving data
        self.threadwatcher = t_watch
        self.id = id

        self.exec = ExecutionClass(queue_for_rov, manual_flag)  # For manual driving
        self.camera = CameraManager()
        self.w = None  # SecondWindow()
        # self.gir_verdier = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Might be used for later

        self.timer = QTimer()  # Create a timer
        self.timer.timeout.connect(
            self.update_gui_data
        )  # Connect the timer to the function that updates the gui
        self.timer.start(100)  # Adjust the interval to your needs
        self.manual = True  # For manual driving

        # Getting values from the gui
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

    # Css styling used for cases
    Gradient = "background-color: #444444; color: #FFFFFF; border-radius: 10px;"
    errorGradient = "background-color: #FF9999; color: #FF0000; border: 1px solid #FF0000; border-radius: 10px;"
    over60 = "border: 2px solid red;"
    over50 = "border: 2px solid orange;"
    over40 = "border: 2px solid yellow;"
    under40 = " border: 2px solid #1E90FF;"

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
                self.exec.show_all_cameras()
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
            self.decideGUIUpdate(sensordata)

    def show_new_window(self, checked):
        if self.w is None:
            self.w = SecondWindow(self)
            self.w.show()
        else:
            print("window already open")

    def connectFunctions(self):
        # Show new window with pictures
        self.showNewWindow.clicked.connect(self.show_new_window)

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
        self.sliderCamVinkel.valueChanged.connect(self.camVinkelUpdate)

        # Lys
        self.slider_lys_forward.valueChanged.connect(self.update_label_and_print_value)
        self.slider_lys_down.valueChanged.connect(
            self.update_label_and_print_value_down
        )
        self.btnTopLys.clicked.connect(lambda: self.front_light_on())
        self.btnBunnLys.clicked.connect(lambda: self.bottom_light_on())

        # Sikringer
        self.btnResetThruster.clicked.connect(lambda: self.reset_12V_thruster_fuse())
        self.btnResetManipulator.clicked.connect(
            lambda: self.reset_12V_manipulator_fuse()
        )

        # IMU
        self.btnKalibrerIMU.clicked.connect(lambda: self.calibrate_IMU())

        # Dybde
        self.btnNullpunktDybde.clicked.connect(lambda: self.reset_depth())

        # Vinkler
        self.btnNullpunktVinkler.clicked.connect(lambda: self.reset_angles())

        # Regulation
        self.btnRegTuning.clicked.connect(lambda: self.updateRegulatorTuning())
        self.btnRegOn.clicked.connect(lambda: self.toogle_regulator_all())
        self.btnRullOn.clicked.connect(lambda: self.toggle_rull_reg())
        self.btnStampOn.clicked.connect(lambda: self.toggle_stamp_reg())
        self.btnDybdeOn.clicked.connect(lambda: self.toggle_dybde_reg())

        # Lyd
        self.btnTestSound.clicked.connect(lambda: self.play_sound(True))
        self.btnStopSound.clicked.connect(lambda: self.play_sound(False))

    def gui_manipulator_state_update(self, sensordata):
        self.toggle_mani.setChecked(sensordata[0])

    def reset_5V_fuse2(self):
        reset_fuse_byte = [0] * 8
        reset_fuse_byte[0] |= 1 << 0  # reset bit 0
        print("Resetting 5V Fuse")
        values = {"reset_controls": reset_fuse_byte}
        print(("Want to send", 97, reset_fuse_byte))
        self.queue.put((4, values))

    def reset_12V_thruster_fuse(self):
        reset_fuse_byte = [0] * 8
        reset_fuse_byte[0] |= 1 << 0  # reset bit 0
        print("Resetting 12V Thruster Fuse")
        values = {"reset_controls_thruster": reset_fuse_byte}
        print(("Want to send", 98, reset_fuse_byte))
        self.queue.put((5, values))

    def reset_12V_manipulator_fuse(self):
        reset_fuse_byte = [0] * 8
        reset_fuse_byte[0] |= 1 << 0  # reset bit 0
        print("Resetting 12V Manipulator Fuse")
        values = {"reset_controls_manipulator": reset_fuse_byte}
        print(("Want to send", 99, reset_fuse_byte))
        self.queue.put((6, values))

    def reset_depth(self):
        reset_depth_byte = [0] * 8
        reset_depth_byte[0] |= 1 << 0  # reset bit 0
        print("Resetting Depth")
        values = {"reset_depth": reset_depth_byte}
        self.queue.put((7, values))
        print(("Want to send", 66, reset_depth_byte))

    def reset_angles(self):
        reset_angles_byte = [0] * 8
        reset_angles_byte[0] |= 1 << 1  # reset bit 1
        print("Resetting Angles")
        values = {"reset_angles": reset_angles_byte}
        print(("Want to send", 66, reset_angles_byte))
        self.queue.put((8, values))

    def calibrate_IMU(self):
        calibrate_IMU_byte = [0] * 8
        calibrate_IMU_byte[0] |= 1 << 2  # reset bit 2
        print("Kalibrerer IMU")
        values = {"kalibrer_IMU": calibrate_IMU_byte}
        print(("Want to send", 66, calibrate_IMU_byte))
        self.queue.put((9, values))

    def update_label_and_print_value(self, value):
        set_light_byte = [0] * 8
        set_light_byte[1] = value
        values = {"slider_top_light": set_light_byte}
        print((f"Want to send", 98, set_light_byte))
        self.queue.put((17, values))
        print("Slider value:", value)

    def update_label_and_print_value_down(self, value):
        set_light_byte = [0] * 8
        set_light_byte[1] = value
        values = {"slider_bottom_light": set_light_byte}
        print((f"Want to send", 99, set_light_byte))
        self.queue.put((18, values))
        print(value)

    def updateRegulatorTuning(self):
        reguleringDropdown = self.reguleringDropdown.currentText()

        try:
            input_value = float(self.tuningInput.text())
        except ValueError:
            self.lastSent.setText("Input value must be a number")
            return
        regulatorValues = {
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

        value = regulatorValues.get(reguleringDropdown, None)
        update_regulator_tuning = [int(value), input_value]
        print(("Want to send", 42, update_regulator_tuning))
        values = {"update_regulator_tuning": update_regulator_tuning}
        self.queue.put((10, values))

        self.lastSent.setText(
            f" Values : ({reguleringDropdown} {input_value}) was sent to ROV"
        )

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

    def toggle_rull_reg(self):
        self.toggle_felles_regulator[0] ^= 1 << 0
        if self.toggle_felles_regulator[0] == (1 << 0):
            print("rull på")
        elif self.toggle_felles_regulator[0] == (0 << 0):
            print("rull av")
        print(("Want to send", 32, self.toggle_felles_regulator))
        values = {"toggle_rull_reg": self.toggle_felles_regulator}
        self.queue.put((12, values))

    def toggle_stamp_reg(self):
        self.toggle_felles_regulator[0] ^= 1 << 2
        if self.toggle_felles_regulator[0] == (1 << 2):
            print("stamp på")
        elif self.toggle_felles_regulator[0] == (0 << 2):
            print("stamp av")
        print(("Want to send", 32, self.toggle_felles_regulator))
        values = {"toggle_rull_reg": self.toggle_felles_regulator}
        self.queue.put((12, values))

    def toggle_dybde_reg(self):
        self.toggle_felles_regulator[0] ^= 1 << 3
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

    def camVinkelUpdate(self, value):
        self.labelKameraVinkel.setText(f"{value}°")
        values = {"tilt": value}
        self.queue.put((19, values))

    def decideGUIUpdate(self, sensordata):
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

    def play_sound(self, should_play: bool):
        self.sound_worker.play.emit(should_play)

    def closeEvent(self, event):
        self.sound_worker_thread.quit()
        self.sound_worker_thread.wait()

    def on_player_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.player.stateChanged.disconnect(self.on_player_state_changed)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.lydFil)))
            self.player.play()

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
        alarmTextsIMU = []
        for i in range(len(sensordata[0])):
            if sensordata[0][i] == True:
                self.currentIMUAlarms.add(i)
                alarmTextsIMU.append(imuErrors[i])
            elif sensordata[0][i] == False and i in self.currentIMUAlarms:
                self.currentIMUAlarms.remove(i)
        if alarmTextsIMU:
            labelIMUAlarm.setText(", ".join(alarmTextsIMU))
            labelIMUAlarm.setStyleSheet(self.errorGradient)
        else:
            labelIMUAlarm.setText("")
            labelIMUAlarm.setStyleSheet("")  # Reset style

        # Update Temp alarms
        alarmTextsTemp = []
        for i in range(len(sensordata[1])):
            if sensordata[1][i] == True:
                self.currentTempAlarms.add(i)
                alarmTextsTemp.append(tempErrors[i])
            elif sensordata[1][i] == False and i in self.currentTempAlarms:
                self.currentTempAlarms.remove(i)
        if alarmTextsTemp:
            labelTempAlarm.setText(", ".join(alarmTextsTemp))
            labelTempAlarm.setStyleSheet(self.errorGradient)
        else:
            labelTempAlarm.setText("")
            labelTempAlarm.setStyleSheet("")  # Reset style

        # Update Trykk alarms
        alarmTextsTrykk = []
        for i in range(len(sensordata[2])):
            if sensordata[2][i] == True:
                self.currentTrykkAlarms.add(i)
                alarmTextsTrykk.append(trykkErrors[i])
            elif sensordata[2][i] == False and i in self.currentTrykkAlarms:
                self.currentTrykkAlarms.remove(i)
        if alarmTextsTrykk:
            labelTrykkAlarm.setText(", ".join(alarmTextsTrykk))
            labelTrykkAlarm.setStyleSheet(self.errorGradient)
        else:
            labelTrykkAlarm.setText("")
            labelTrykkAlarm.setStyleSheet("")  # Reset style

        # Update Lekkasje alarms
        alarmTextsLekkasje = []
        for i in range(len(sensordata[3])):
            if sensordata[3][i] == True:
                self.currentLekkasjeAlarms.add(i)
                alarmTextsLekkasje.append(lekkasjeErrors[i])
                self.play_sound(True)
            elif sensordata[3][i] == False and i in self.currentLekkasjeAlarms:
                self.currentLekkasjeAlarms.remove(i)
                self.play_sound(False)
        if alarmTextsLekkasje:
            labelLekkasjeAlarm.setText(", ".join(alarmTextsLekkasje))
            labelLekkasjeAlarm.setStyleSheet(self.errorGradient)
        else:
            labelLekkasjeAlarm.setText("")
            labelLekkasjeAlarm.setStyleSheet("")  # Reset style

    def guiVinkelUpdate(self, sensordata):
        vinkel_liste: list[QLabel] = [
            self.labelRull,
            self.labelStamp,
            self.labelGir,
        ]
        for i, label in enumerate(vinkel_liste):
            label.setText(str(round(sensordata[i] / 100, 2)) + "°")

    def dybdeTempUpdate(self, sensordata):
        labelDybde: QLabel = self.labelDybde

        labelVann: QLabel = self.labelTempVann
        labelSensor: QLabel = self.labelTempSensorkort

        labelDybde.setText(str(round(sensordata[0], 2)) + "cm")
        labelVann.setText(str(round(sensordata[1], 2)) + "°C")

        temp_sensor = round(sensordata[2] / 100, 2)
        labelSensor.setText(str(temp_sensor) + "°C")

        if temp_sensor >= 60:
            labelSensor.setStyleSheet(self.over60)
        elif temp_sensor >= 50:
            labelSensor.setStyleSheet(self.over50)
        elif temp_sensor >= 40:
            labelSensor.setStyleSheet(self.over40)
        else:
            labelSensor.setStyleSheet(self.under40)

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

        temp_manipulator = round(sensordata[1] / 100, 2)
        labelTemp.setText(str(temp_manipulator) + "°C")

        if temp_manipulator >= 60:
            labelTemp.setStyleSheet(self.over60)
        elif temp_manipulator >= 50:
            labelTemp.setStyleSheet(self.over50)
        elif temp_manipulator >= 40:
            labelTemp.setStyleSheet(self.over40)
        else:
            labelTemp.setStyleSheet(self.under40)

        alarmTexts = []
        for i in range(3):
            if sensordata[2][i] == True:
                self.currentManipulatorAlarms.add(i)
                alarmTexts.append(self.kraftFeilkoder[i])
            elif sensordata[2][i] == False and i in self.currentManipulatorAlarms:
                self.currentManipulatorAlarms.remove(i)

        if alarmTexts:
            labelSikring.setText(", ".join(alarmTexts))
            labelSikring.setStyleSheet(self.errorGradient)
        else:
            labelSikring.setText("")

    def thruster12VUpdate(self, sensordata):
        labelKraft: QLabel = self.labelThrusterKraft
        labelTemp: QLabel = self.labelThruster12VTemp
        labelSikring: QLabel = self.labelThrusterSikring

        labelKraft.setText(str(round(sensordata[0] / 1000, 2)) + "A")

        temp_thruster = round(sensordata[1] / 100, 2)
        labelTemp.setText(str(temp_thruster) + "°C")

        if temp_thruster >= 60:
            labelTemp.setStyleSheet(self.over60)
        elif temp_thruster >= 50:
            labelTemp.setStyleSheet(self.over50)
        elif temp_thruster >= 40:
            labelTemp.setStyleSheet(self.over40)
        else:
            labelTemp.setStyleSheet(self.under40)

        alarmTexts = []
        for i in range(3):
            if sensordata[2][i] == True:
                self.currentThrusterAlarms.add(i)
                alarmTexts.append(self.kraftFeilkoder[i])
            elif sensordata[2][i] == False and i in self.currentThrusterAlarms:
                self.currentThrusterAlarms.remove(i)

        if alarmTexts:
            labelSikring.setText(", ".join(alarmTexts))
            labelSikring.setStyleSheet(self.errorGradient)
        else:
            labelSikring.setText("")

    def kraft5VUpdate(self, sensordata):
        labelTemp: QLabel = self.labelKraft5VTemp

        temp_kraft = round(sensordata[1] / 100, 2)
        labelTemp.setText(str(temp_kraft) + "°C")

        if temp_kraft >= 60:
            labelTemp.setStyleSheet(self.over60)
        elif temp_kraft >= 50:
            labelTemp.setStyleSheet(self.over50)
        elif temp_kraft >= 40:
            labelTemp.setStyleSheet(self.over40)
        else:
            labelTemp.setStyleSheet(self.under40)

    def reguleringMotorTempUpdate(self, sensordata):
        labelRegulering: QLabel = self.labelReguleringTemp
        labelMotor: QLabel = self.labelMotorTemp
        labelDybde: QLabel = self.labelDybdeSettpunkt

        temp_regulering = round(sensordata[0] / 100, 2)
        labelRegulering.setText(str(temp_regulering) + "°C")

        if temp_regulering > 60:
            labelRegulering.setStyleSheet(self.over60)
        elif temp_regulering > 50:
            labelRegulering.setStyleSheet(self.over50)
        elif temp_regulering > 40:
            labelRegulering.setStyleSheet(self.over40)
        else:
            labelRegulering.setStyleSheet(self.under40)

        temp_motor = round(sensordata[1] / 100, 2)
        labelMotor.setText(str(temp_motor) + "°C")

        if temp_motor >= 60:
            labelMotor.setStyleSheet(self.over60)
        elif temp_motor >= 50:
            labelMotor.setStyleSheet(self.over50)
        elif temp_motor >= 40:
            labelMotor.setStyleSheet(self.over40)
        else:
            labelMotor.setStyleSheet(self.under40)

        labelDybde.setText(str(round(sensordata[2] / 100, 2)) + "cm")

    def TempKomKontrollerUpdate(self, sensordata):
        labelTemp: QLabel = self.labelTempKomKontroller

        temp_kom = round(sensordata, 2)
        labelTemp.setText(str(temp_kom) + "°C")

        if temp_kom >= 60:
            labelTemp.setStyleSheet(self.over60)
        elif temp_kom >= 50:
            labelTemp.setStyleSheet(self.over50)
        elif temp_kom >= 40:
            labelTemp.setStyleSheet(self.over40)
        else:
            labelTemp.setStyleSheet(self.under40)


def run(conn, queue_for_rov, manual_flag, t_watch: Threadwatcher, id):
    app = QtWidgets.QApplication(
        sys.argv
    )  # Create an instance of QtWidgets.QApplication

    # Create an instance of our class
    win = Window(conn, queue_for_rov, manual_flag, t_watch, id)
    GLOBAL_STATE = False
    win.show()  # Show the form

    app.exec()


from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import os


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

        self.image_directory = "camerafeed/output"
        self.image_files = sorted(
            [
                f
                for f in os.listdir(self.image_directory)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
            ]
        )
        self.current_image_index = 0

        self.update_image()

        # Call connectFunctions() after initializing all the necessary attributes
        self.connectFunctions()

    def closeEvent(self, event):
        self.main_window.w = None
        event.accept()

    def connectFunctions(self):
        self.lastPic.clicked.connect(self.load_previous_image)
        self.nextPic.clicked.connect(self.load_next_image)

    def load_previous_image(self):
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.image_files) - 1
        self.update_image()

    def load_next_image(self):
        self.current_image_index += 1
        if self.current_image_index >= len(self.image_files):
            self.current_image_index = 0
        self.update_image()

    def update_image(self):
        current_image_path = os.path.join(
            self.image_directory, self.image_files[self.current_image_index]
        )
        pixmap = QPixmap(current_image_path)
        window_size = self.size()  # Get the size of the window
        scaled_pixmap = pixmap.scaled(
            window_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.pic.setPixmap(scaled_pixmap)
        self.pic.setFixedSize(scaled_pixmap.size())


# A class for playing sound in a separate thread
class SoundWorker(QObject):
    play = pyqtSignal(bool)

    def __init__(self, lydFil):
        super().__init__()
        self.player = QMediaPlayer()
        self.lydFil = lydFil

        self.play.connect(self.on_play)
        self.player.stateChanged.connect(self.on_player_state_changed)

    def on_play(self, should_play: bool):
        if should_play:
            if self.player.state() != QMediaPlayer.PlayingState:
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.lydFil)))
                self.player.play()
        else:
            self.player.stop()

    def on_player_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.lydFil)))
            self.player.play()


# A class for communication between threads
class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(dict)


if __name__ == "__main__":
    run()
