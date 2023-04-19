import threading
import time
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


X_AXIS = 1
Y_AKSE = 0
Z_AKSE = 6
R_AKSE = 2

class CameraClass:
    def __init__(self) -> None:
        self.frame_down = None
        self.frame_manip = None
        self.frame_stereoL = None
        self.frame_stereoR = None
        self.frame_manual = None
        self.frame_test = None
        
        self.cam_down = None
        self.cam_stereoL = None
        self.cam_stereoR = None
        self.cam_manip = None
        self.cam_test = None
        self.cam_manual = None
        self.recording = False
        

    def get_frame_down(self):
        _, self.frame_down = self.cam_down.read()
        
        return self.frame_down
        
    def get_frame_manip(self):
        _, self.frame_manip = self.cam_manip.read()
        
        return self.frame_manip
    
    def get_frame_stereo_L(self):
        _, self.frame_stereoL = self.cam_stereoL.read()
        
        return self.frame_stereoL

    def get_frame_stereo_R(self):
        _, self.frame_stereoR = self.cam_stereoR.read()
        return self.frame_stereoR
        
    def get_frame_manual(self):
        _, self.frame_manual = self.cam_manual.read()
        
        return self.frame_manual
    
    def get_frame_test(self):
        _, self.frame_test = self.cam_test.read()
        
        return self.frame_test
        
    def start_down_cam(self):
        print("Starting down camera")
        gst_feed_down = "-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5002 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
        self.cam_down = cv2.VideoCapture(gst_feed_down, cv2.CAP_GSTREAMER)
        if self.cam_down.isOpened():
            print("Down camera started")
        _, self.frame_down = self.cam_down.read()
        
    def start_stereo_cam_L(self):
        print("Starting stereo camera L")
        gst_feed_stereoL = "-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
        self.cam_stereoL = cv2.VideoCapture(gst_feed_stereoL, cv2.CAP_GSTREAMER)
        if self.cam_stereoL.isOpened():
            print("StereoL camera started")
            
        _, self.frame_stereoL = self.cam_stereoL.read()
        
    def start_stereo_cam_R(self):
        print("Starting stereo camera R")
        gst_feed_stereoR = "-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5001 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
        self.cam_stereoR = cv2.VideoCapture(gst_feed_stereoR, cv2.CAP_GSTREAMER)
        if self.cam_stereoR.isOpened():
            print("StereoR camera started")
        
        _, self.frame_stereoR = self.cam_stereoR.read()
        
    def start_manip_cam(self):
        print("Starting manip camera")
        gst_feed_manip = "-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5003 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"

        self.cam_manip = cv2.VideoCapture(gst_feed_manip, cv2.CAP_GSTREAMER)
        if self.cam_manip.isOpened():
            print("Manip camera started")
        _, self.frame_manip = self.cam_manip.read()
        
        
    def start_manual_cam(self):
        print("Starting manual camera")
        self.cam_manual = cv2.VideoCapture(0)
        if self.cam_manual.isOpened():
            print("Manual camera started")
        
    def start_test_cam(self):
        print("Starting test camera")
        self.cam_test = cv2.VideoCapture(0)
        if self.cam_test.isOpened():
            print("Test camera started")
        
    def start(self):
        # self.start_down_cam()
        self.start_stereo_cam_L()
        self.start_stereo_cam_R()
        # self.start_manip_cam()
        # self.start_manual_cam()

    def close_all(self):
        if self.cam_down is not None and self.cam_down.isOpened():
            self.cam_down.release()
            
        if self.cam_stereoL is not None and self.cam_stereoL.isOpened():
            self.cam_stereoL.release()
            
        if self.cam_stereoR is not None and self.cam_stereoR.isOpened():
            self.cam_stereoR.release()
            
        if self.cam_manip is not None and self.cam_manip.isOpened():
            self.cam_manip.release()
            
        if self.cam_manual is not None and self.cam_manual.isOpened():
            self.cam_manual.release()
            
        if self.cam_test is not None and self.cam_test.isOpened():
            self.cam_test.release()
        
    def setup_video(self, name):
        self.videoresult = cv2.VideoWriter(f'camerafeed/output/{name}.avi', cv2.VideoWriter_fourcc(
            *'MJPG'), 10, (int(self.cam_manual.get(3)), int(self.cam_manual.get(4))))

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
    def __init__(self, driving_queue, manual_flag):
        self.AutonomousTransect = AutonomousTransect()
        self.Docking = AutonomousDocking()
        self.Seagrass = SeagrassMonitor()
        self.Camera = CameraClass()
        self.counter = 0
        self.done = False
        # self.Camera.start()
        self.manual_flag = manual_flag
        self.driving_queue = driving_queue

    def update_down(self):
        self.frame_down = self.Camera.get_frame_down()
        
    def update_stereo_L(self):
        self.frame_stereoL = self.Camera.get_frame_stereo_L()
        
    def update_stereo_R(self):
        self.frame_stereoR = self.Camera.get_frame_stereo_R()
        
    def update_manip(self):
        self.frame_manip = self.Camera.get_frame_manip()
        
    def update_manual(self):
        self.frame_manual = self.Camera.get_frame_manual()

    def update_test_cam(self):
        self.frame_test = self.Camera.get_frame_test()
        
    def show(self, frame, name="frame"):
        cv2.imshow(name, frame)
        if cv2.waitKey(1) == ord("q"):
            self.stop_everything()
            
    def testing_for_torr(self):
        self.done = False
        while not self.done:
            self.update_stereo_L()
            self.update_stereo_R()
            self.show(self.frame_stereoL, "StereoL")
            self.show(self.frame_stereoR, "StereoR")
            QApplication.processEvents()
            
    def camera_test(self):
        while self.done:
            # self.update_manual()
            self.update_down()
            self.update_stereo_L()
            # self.update_stereo_R()
            # self.update_manip()
            
            self.show(self.frame_down, "Down")
            # self.show(self.frame_manual, "Manual")
            self.show(self.frame_stereoL, "StereoL")
            # self.show(self.frame_stereoR, "StereoR")
            # self.show(self.frame_manip, "Manip")
            QApplication.processEvents()

    def save_image(self):
        cv2.imwrite("camerafeed/output/output_image.jpg", self.frame.copy())
        
    def send_data_test(self):
        self.done = False
        start = 0
        while not self.done:
            cur_time = time.time()
            if (cur_time - start) > 0.02:
                random_data = [random.randint(0,10) for _ in range(8)]
                self.send_data_to_rov(random_data)
                
                QApplication.processEvents()
                start = time.time()
        
    def sleep_func(self):
        threading.Timer(1000, self.sleep_func).start()

    def transect(self):
        self.done = False
        self.Camera.start_down_cam() # TODO should be down frame
        while not self.done and self.manual_flag.value == 0:
            self.update_down() # TODO Should be down frame
            transect_frame, driving_data_packet = self.AutonomousTransect.run(self.frame_down)
            self.show(transect_frame, "Transect")
            self.send_data_to_rov(driving_data_packet)
            QApplication.processEvents()
        else:
            self.stop_everything()

    def seagrass(self):
        growth = self.Seagrass.run(self.frame.copy())
        return growth

    def docking(self):
        self.done = False
        self.Camera.start_stereo_cam_L()
        self.Camera.start_stereo_cam_R() # TODO shoould be down camera
        while not self.done:
            # Needs stereo L, and Down Cameras
            self.update_stereo_R()
            self.update_stereo_L() # TODO should be down camera
            docking_frame, frame_under, driving_data_packet = self.Docking.run(self.frame_stereoL, self.frame_stereoR) # TODO should be down camera
            self.show(docking_frame, "Docking")
            self.show(frame_under, "Frame Under")
            self.driving_queue.put(driving_data_packet)
            QApplication.processEvents()
            # self.show(frame_under, "Frame Under")
            
    def send_data_to_rov(self, datapacket):
        data_to_send = {"autonomdata": datapacket}
        self.driving_queue.put((2, data_to_send))

    def normal_camera(self):
        self.done = False
        self.Camera.start_manual_cam()
        while not self.done:
            self.update_manual()
            self.show(self.frame_manual, "Manual")
            QApplication.processEvents()
            
    def stop_everything(self):
        print("Stopping other processes, returning to manual control")
        self.done = True
        cv2.destroyAllWindows()
        self.Camera.close_all()

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
            self.update_manual()
            self.show(self.frame_manual.copy(), "Recording...")
            self.Camera.record_video(self.frame_manual.copy())
            QApplication.processEvents()
    
    def save_image(self):
        self.Camera.save_image(self.frame_manual.copy())
        print("Image saved")
        

if __name__ == "__main__":
    cam = CameraClass()
    execution = ExecutionClass()
    while True:
        execution.update_stereo()
        # execution.show(execution.frame_down, "Down")
        execution.show(execution.frame_stereoL, "StereoL")
        execution.show(execution.frame_stereoR, "StereoR")
        # execution.show(execution.frame_manip, "Manip")
