import time
from camerafeed.Main_Classes.autonomous_transect_main import AutonomousTransect
from camerafeed.Main_Classes.grass_monitor_main import SeagrassMonitor
from camerafeed.Main_Classes.autonomous_docking_main import AutonomousDocking
import cv2
import multiprocessing as mp
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Camera:
    def __init__(self) -> None:
        self.cam = cv2.VideoCapture(0)
        self.frame = self.cam.read()[1]
        self.recording = False

    def get_frame(self):
        while True:
            success, self.frame = self.cam.read()
            print("Printer frames")
            yield self.frame

    def setup_video(self, name):
        self.videoresult = cv2.VideoWriter(f'camerafeed/output/{name}.avi', cv2.VideoWriter_fourcc(
            *'MJPG'), 10, (int(self.cam.get(3)), int(self.cam.get(4))))

    # Run this to start recording, and do a keyboard interrupt (ctrl + c) to stop recording

    def record_video(self, frame):
        if not self.recording:
            self.setup_video("output_video")
            self.recording = True

        try:
            self.videoresult.write(frame)
        except KeyboardInterrupt:
            self.videoresult.release()


class ExecutionClass:
    def __init__(self):
        self.AutonomousTransect = AutonomousTransect()
        self.Docking = AutonomousDocking()
        self.Seagrass = SeagrassMonitor()

    def show(self, frame, name="frame"):
        cv2.imshow(name, frame)
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            raise KeyboardInterrupt

    def save_image(self):
        cv2.imwrite("camerafeed/output/output_image.jpg", self.frame)

    def transect(self):
        # transect_frame, driving_data_packet, frog_counter = self.AutonomousTransect.run(
        #    frame.copy())
        print("Running transect")
        #print("Frogs found", frog_counter)
        #self.show(transect_frame, "Transect")
        # return driving_data_packet

    def seagrass(self):
        print("Seagrass running")
        #growth = self.Seagrass.run(frame.copy())
        # return growth

    def docking(self):
        self.done = False
        while not self.done:

            # docking_frame, frame_under, driving_data_packet = self.Docking.run(
            #    frame.copy())
            print("Docking running")
            time.sleep(1)
            QApplication.processEvents()
        #self.show(docking_frame, "Docking")
        #self.show(frame_under, "Frame Under")
        # return driving_data_packet

    def manual_driving(self):
        self.done = True
        print("Stop Processes.")


if __name__ == "__main__":
    cam = Camera()
    execution = ExecutionClass()
    while True:
        frame = cam.get_frame()
        execution.show(frame)
        # cam.record_video(frame)
        execution.transect(frame)
