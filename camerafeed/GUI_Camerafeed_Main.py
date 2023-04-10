from camerafeed.Main_Classes.autonomous_transect_main import AutonomousTransect
from camerafeed.Main_Classes.grass_monitor_main import SeagrassMonitor
from camerafeed.Main_Classes.autonomous_docking_main import AutonomousDocking
import cv2
import multiprocessing as mp
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
import random


class CameraClass:
    def __init__(self) -> None:
        self.frame = None

    def get_frame(self):
        success, self.frame = self.cam.read()
        if success:
            return self.frame

        # cv2.imshow("frame", self.frame)
        # if cv2.waitKey(1) == ord("q"):
        #     cv2.destroyAllWindows()
        #     raise KeyboardInterrupt

    def start(self):
        print("Camera has been started")
        self.cam = cv2.VideoCapture(0)
        self.frame = self.get_frame()
        self.recording = False

    def setup_video(self, name):
        self.videoresult = cv2.VideoWriter(f'camerafeed/output/{name}.avi', cv2.VideoWriter_fourcc(
            *'MJPG'), 10, (int(self.cam.get(3)), int(self.cam.get(4))))

    # Run this to start recording, and do a keyboard interrupt (ctrl + c) to stop recording

    def record_video(self, frame):
        if not self.recording:
            self.setup_video(f"MyCam{datetime.datetime.now()}")
            self.recording = True
        if self.recording:
            self.videoresult.write(frame)
        else:
            self.videoresult.release()
    
    def save_image(self, frame):
        cv2.imwrite(f"camerafeed/output/Img{datetime.datetime.now()}.jpg", frame)
        
class ExecutionClass:
    def __init__(self, driving_queue):
        self.AutonomousTransect = AutonomousTransect()
        self.Docking = AutonomousDocking()
        self.Seagrass = SeagrassMonitor()
        self.Camera = CameraClass()
        self.counter = 0
        self.done = False
        self.Camera.start()
        self.driving_queue = driving_queue

    def update(self):
        self.frame = self.Camera.get_frame()

    def show(self, frame, name="frame"):
        self.update()
        if frame.any() == None:
            frame = self.frame
        cv2.imshow(name, frame)
        if cv2.waitKey(1) == ord("q"):
            self.manual()

    def save_image(self):
        cv2.imwrite("camerafeed/output/output_image.jpg", self.frame.copy())
        
    def send_data_test(self):
        while True:
            random_data = [40, [random.randint(0,10) for i in range(8)]]
            self.driving_queue.put(random_data)
            QApplication.processEvents()

    def transect(self):
        self.done = False
        while not self.done:
            self.update()
            transect_frame, driving_data_packet = self.AutonomousTransect.run(
                self.frame.copy())
            self.show(transect_frame, "Transect")
            self.driving_queue.put(driving_data_packet)
            QApplication.processEvents()

    def seagrass(self):
        growth = self.Seagrass.run(self.frame.copy())
        return growth

    def docking(self):
        self.done = False
        while not self.done:

            self.update()
            docking_frame, frame_under, driving_data_packet = self.Docking.run(
                self.frame.copy())
            self.show(docking_frame, "Docking")
            QApplication.processEvents()
            # self.show(frame_under, "Frame Under")
        return driving_data_packet

    def manual(self):
        print("Stopping other processes, returning to manual control")
        cv2.destroyAllWindows()
        self.done = True

    def transect_test(self):
        print("Running Transect!")
        
    def record(self):
        self.done = False
        if self.Camera.recording:
            self.Camera.recording = False
            cv2.destroyWindow("Recording...")
            print("Recording stopped")
            self.done = True

        while not self.done:
            self.update()
            self.show(self.frame.copy(), "Recording...")
            self.Camera.record_video(self.frame)
            QApplication.processEvents()
    
    def save_image(self):
        self.Camera.save_image(self.frame.copy())
        print("Image saved")
        

if __name__ == "__main__":
    cam = CameraClass()
    execution = ExecutionClass()
    while True:
        frame = cam.get_frame()
        execution.show(frame)
        cam.record_video(frame)
        # execution.transect(frame)
