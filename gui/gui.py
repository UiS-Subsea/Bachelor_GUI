import multiprocessing
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets, Qt, uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QCheckBox, QLabel, QMessageBox
import sys
import threading
from . import guiFunctions as f
from Thread_info import Threadwatcher
import time

class Window(QMainWindow):
    def __init__(
        self,
        pipe_conn_only_rcv,
        queue: multiprocessing.Queue,
        t_watch: Threadwatcher,
        id: int,
        parent=None,
    ):

        super().__init__(parent)
        uic.loadUi("gui/Subsea.ui", self)
        self.connectFunctions()

        regulering_status_wait_counter = 0
        self.lekkasje_varsel_is_running = False
        self.ID_RESET_DEPTH = 66
        # Queue and pipe
        self.queue: multiprocessing.Queue = (
            queue  
        )
        
        self.pipe_conn_only_rcv = pipe_conn_only_rcv  # pipe_conn_only_rcv is a pipe connection that only receives data
        # Threadwatcher
        self.t_watch: Threadwatcher = t_watch  # t_watch is a threadwatcher object
        self.id = id  # id is an id that is used to identify the thread

        self.gir_verdier = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


        self.receive = threading.Thread(
            target=self.receive_sensordata, daemon=True, args=(self.pipe_conn_only_rcv,)
        )
        self.receive.start()
        

        self.w=None#SecondWindow() #


        # Buttons
    def show_new_window(self, checked):
        if self.w is None:
            self.w = SecondWindow(self)
            self.w.show()
        else:
            print("window already open")

    def connectFunctions(self,ID_RESET_DEPTH=66):
        #window2
        self.showNewWindowButton.clicked.connect(self.show_new_window)
    
        #Kjøremodus
        self.btnManuell.clicked.connect(lambda: f.manuellKjoring(self))
        self.btnAutonom.clicked.connect(lambda: f.autonomDocking(self))
        self.btnFrogCount.clicked.connect(lambda: f.frogCount(self))
        
        #Sikringer
        self.btnReset5V.clicked.connect(lambda: f.reset5V(self))
        self.btnResetThruster.clicked.connect(lambda: f.resetThruster(self))
        self.btnResetManipulator.clicked.connect(lambda :f.resetManipulator(self))
        
        #IMU
        self.btnKalibrerIMU.clicked.connect(lambda: f.kalibrerIMU(self))
        
        #Dybde
        self.btnNullpunktDybde.clicked.connect(lambda: f.nullpunktDybde(self))
        
        #Vinkler
        self.btnNullpunktVinkler.clicked.connect(lambda: f.nullpunktVinkler(self))
        
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

    def gui_manipulator_state_update(self, sensordata):
        self.toggle_mani.setChecked(sensordata[0])

    def decide_gui_update(self, sensordata):
        self.sensor_update_function = {
            "lekk_temp": self.gui_lekk_temp_update,
            "thrust": self.gui_thrust_update,
            # "accel": self.gui_acceleration_update,
            # "gyro": self.gui_gyro_update,
            # "time": self.gui_time_update,
            "manipulator": self.gui_manipulator_update,
            "power_consumption": self.gui_watt_update,
            "manipulator_toggled": self.gui_manipulator_state_update,
            # "regulator_strom_status": self.regulator_strom_status,
            # "regulering_status": self.gui_regulering_state_update,
            # "settpunkt": self.print_data
        }
        for key in sensordata.keys():
            if key in self.sensor_update_function:
                self.sensor_update_function[key](sensordata[key])

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

        # self.label_effekt_manipulator_2.setText(str(round(sensordata[1])) + " W")
        # self.label_effekt_elektronikk_2.setText(str(round(sensordata[2])) +" W")

    def update_round_percent_visualizer(self, value, text_label):
        text_label.setText(str(value))
        # self.round_percent_visualizer.setValue(value)
        # self.round_percent_visualizer.setFormat(str(value) + "%")

    def gui_thrust_update(self, sensordata):
        print(f"thrust update: {sensordata = }")  # Print sensordata
        for i in range(len(sensordata)):  # For each value in sensordata
            if sensordata[i] > 100:  # If the value is greater than 100
                sensordata[i] = 100  # Set the value to 100

        # Update the labels
        self.update_round_percent_visualizer(sensordata[0], self.thrust_label_1)
        self.update_round_percent_visualizer(sensordata[1], self.thrust_label_2)
        self.update_round_percent_visualizer(sensordata[2], self.thrust_label_3)
        self.update_round_percent_visualizer(sensordata[3], self.thrust_label_4)
        self.update_round_percent_visualizer(sensordata[4], self.thrust_label_5)
        self.update_round_percent_visualizer(sensordata[5], self.thrust_label_6)
        self.update_round_percent_visualizer(sensordata[6], self.thrust_label_7)
        self.update_round_percent_visualizer(sensordata[7], self.thrust_label_8)

    def gui_lekk_temp_update(self, sensordata):
        # self.check_data_types(sensordata["lekk_temp"], (int, float, float, float))
        print(f"ran gui_lekk_temp_update {sensordata = }")
        print(f"{sensordata =}")

        temp_label_list: list[QLabel] = [
            self.labelTempHovedkort,
            self.labelTempKraftkort,
            self.labelTempSensorkort,
            self.labelGjSnittROV,
        ]

        lekkasje_liste: list[bool] = [sensordata[0], sensordata[1], sensordata[2]]
        if not isinstance(lekkasje_liste[0], bool):
            raise TypeError(
                f"Lekkasje sensor 1 has wrong type. {type(lekkasje_liste[0]) = }, {lekkasje_liste[0]} "
            )
        average_temp = round(sum((sensordata[3:6])) / 3)
        sensordata.append(average_temp)

        for i in range(4):
            temp_label_list[i].setText(str(sensordata[i + 3]))
        if (
            sensordata[3] > 61
        ):  # Høyeste temp sett ved kjøring i bassenget på skolen | Hovedkort
            temp_label_list[i].setStyleSheet(
                "background-color: #ff0000; border-radius: 5px; border: 1px solid rgb(30, 30, 30);"
            )
        else:
            temp_label_list[i].setStyleSheet(
                "background-color: rgb(30, 33, 38); border-radius: 5px; border: 1px solid rgb(30, 30, 30);"
            )
        if (
            sensordata[4] > 51
        ):  # Høyeste temp sett ved kjøring i bassenget på skolen | Kraftkort
            temp_label_list[i].setStyleSheet(
                "background-color: #ff0000; border-radius: 5px; border: 1px solid rgb(30, 30, 30);"
            )
        else:
            temp_label_list[i].setStyleSheet(
                "background-color: rgb(30, 33, 38); border-radius: 5px; border: 1px solid rgb(30, 30, 30);"
            )
        if (
            sensordata[5] > 46
        ):  # Høyeste temp sett ved kjøring i bassenget på skolen | Sensorkort
            temp_label_list[i].setStyleSheet(
                "background-color: #ff0000; border-radius: 5px; border: 1px solid rgb(30, 30, 30);"
            )
        else:
            temp_label_list[i].setStyleSheet(
                "background-color: rgb(30, 33, 38); border-radius: 5px; border: 1px solid rgb(30, 30, 30);"
            )

        id_with_lekkasje = []  # List of IDs for sensors with leaks
        for lekkasje_nr, is_lekkasje in enumerate(
            lekkasje_liste
        ):  # For each sensor in the list of leaks
            if not is_lekkasje:  # If the sensor doesn't have a leak
                id_with_lekkasje.append(
                    lekkasje_nr + 1
                )  # Add the sensor's ID to id_with_lekkasje
        if (
            not self.lekkasje_varsel_is_running and len(id_with_lekkasje) > 0
        ):  # If there is no leak alert running and there is a sensor with a leak
            self.lekkasje_varsel_is_running = (
                True  # Set lekkasje_varsel_is_running to True
            )
            threading.Thread(
                target=lambda: self.lekkasje_varsel(id_with_lekkasje)
            ).start()  # Start the leak alert in a separate thread
    
    def lekkasje_varsel(self, sensor_nr_liste):
        self.label_lekkasje_varsel.setMaximumSize(16777215,150)
        self.label_lekkasje_varsel.setMinimumSize(16777215,150)
        self.label_lekkasje_varsel.raise_()
        sensor_nr_liste = [str(item) for item in sensor_nr_liste]
        text = f"Advarsel vannlekkasje oppdaget på sensor: {str(', '.join(sensor_nr_liste))}"
        self.label_lekkasje_varsel.setText(text)
        self.label_lekkasje_varsel.setStyleSheet("QLabel { color: rgba(255, 255, 255, 200); background-color: rgba(179, 32, 36, 200); font-size: 24pt;}")
        if "win" in sys.platform:
            subprocess.call(('./ffplay.exe -autoexit -nodisp ./siren.wav'), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            subprocess.call(('./ffplay', '-autoexit', '-nodisp', './siren.wav'), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        self.label_lekkasje_varsel.setStyleSheet("QLabel { color: rgba(255, 255, 255, 0); background-color: rgba(179, 32, 36, 0); font-size: 24pt;}")
        self.label_lekkasje_varsel.lower()
        self.lekkasje_varsel_is_running = False
        self.label_lekkasje_varsel.setMaximumSize(0,0)
        self.label_lekkasje_varsel.setMinimumSize(0,0)
        
        
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



def run(conn, queue_for_rov, t_watch: Threadwatcher, id):
    # TODO: add suppress qt warnings?

    app = QtWidgets.QApplication(
        sys.argv
    )  # Create an instance of QtWidgets.QApplication

    win = Window(conn, queue_for_rov, t_watch, id)  # Create an instance of our class
    GLOBAL_STATE = False
    win.show()  # Show the form

    app.exec()
    #sys.exit(app.exec())

class SecondWindow(QWidget):
    def __init__(self,main_window,parent=None,):
        super().__init__()
        uic.loadUi("gui/window2.ui", self)
        self.label = QLabel("Camera Window")
        self.main_window = main_window
        self.connectFunctions()

    def closeEvent(self, event):
        self.main_window.w = None
        event.accept()
    
    def connectFunctions(self):
        #Kamera
        self.btnTiltUp.clicked.connect(lambda: f.tiltUp(self))
        self.btnTiltDown.clicked.connect(lambda: f.tiltDown(self))
        self.btnTakePic.clicked.connect(lambda: f.takePic(self))
        self.btnSavePic.clicked.connect(lambda: f.savePic(self))

class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(dict)


if __name__ == "__main__":
    run()
    
