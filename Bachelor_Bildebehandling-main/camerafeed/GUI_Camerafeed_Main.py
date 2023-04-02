from Main_Classes.autonomous_transect_main import AutonomousTransect
from Main_Classes.grass_monitor_main import SeagrassMonitor
from Main_Classes.autonomous_docking_main import AutonomousDocking
import cv2
import multiprocessing as mp

class Camera:
    def __init__(self) -> None:
        self.cam = cv2.VideoCapture(0)
        self.frame = self.cam.read()[1]
        self.recording = False
        
    def get_frame(self):
        success, self.frame = self.cam.read()
        return self.frame
    
    def setup_video(self, name):
        self.videoresult = cv2.VideoWriter(f'camerafeed/output/{name}.avi', cv2.VideoWriter_fourcc(*'MJPG'),10, (int(self.cam.get(3)), int(self.cam.get(4))))


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
        
    def show(self, frame, name = "frame"):
        cv2.imshow(name, frame)
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            raise KeyboardInterrupt
        
    def save_image(self):
        cv2.imwrite("camerafeed/output/output_image.jpg", self.frame)
            
    def transect(self, frame):
        transect_frame, driving_data_packet, frog_counter = self.AutonomousTransect.run(frame.copy())
        print("Frogs found", frog_counter)
        self.show(transect_frame, "Transect")
        return driving_data_packet
            
    def seagrass(self, frame):
        growth = self.Seagrass.run(frame.copy())
        return growth
        
        
    def docking(self, frame):
        docking_frame, frame_under, driving_data_packet = self.Docking.run(frame.copy())
        self.show(docking_frame, "Docking")
        self.show(frame_under, "Frame Under")
        return driving_data_packet
    
   
        

if __name__ == "__main__":
    cam = Camera()
    execution = ExecutionClass()
    while True:
        frame = cam.get_frame()
        execution.show(frame)
        # cam.record_video(frame)
        execution.transect(frame)
        
    
    