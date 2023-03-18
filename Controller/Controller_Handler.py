import multiprocessing
from Threadwatch import Threadwatcher
import threading
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time
import sys
DPAD = 1538         #Kan også bruke pygame.JOYBUTTONDOWN hvis nødvendig
BUTTON_DOWN = 1539
BUTTON_UP = 1540
JOYSTICK = 1536

BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3


def clear_screen():
    pass
    os.system("cls")


class Controller:
    def __init__(self, queue_to_rov: multiprocessing.Queue, t_watch: Threadwatcher, id, joystick_deadzone=15) -> None:
        # Queue that is received in main
        self.queue_to_rov = queue_to_rov
        # t_watch and id is used for closing the process from main
        self.t_watch = t_watch
        self.id = id
        #Variable that decides when we set the controller to be in the center. Used for stopping the controller sending small values when the stick is let go
        self.joystick_deadzone = joystick_deadzone  # deadzone in percent
        # list of all buttons that can be clicked. 1 means it is clicked and 0 is not clicked
        self.rov_buttons = [0]*10

        self.mani_buttons = [0]*10
        # values for all axes of the joysticks (and one "virtual joystick" that combines axes)
        self.rov_joysticks = [0]*7

        self.mani_joysticks = [0]*7
        # tuple for dpad controll. Goes from -1 to 1 on both first and second variable
        self.rov_dpad = (0, 0)

        self.mani_dpad = (0, 0)
        # This is the max value that the controller gives out. Used for normalizing the axis to 1.
        self.controller_stop_point = 1.000030518509476
        # Decides which camera should be moved.
        self.camera_motor = 0
        # Think this is unused
        self.boyancy = 0
        # Variable that is used to see if the controller needs to be reset before trying to connect. On first run we do not need to reset it
        self.first_run = True
        # Map for knowing the name of the button in the self.buttons list 
        self.button_names = {0: "A", 1: "B", 2: "X", 3: "Y", 4: "Left button back", 5: "Right button back", 6: "Back", 7: "Start", 8: "Thumb button left", 9: "Thumb button right"}
        # Initialize the duration timer which says how long since last time the .tick metod was called
        self.duration = -1
        pygame.init()
        # Waits until it finds a controller and tries to connect to it
        self.wait_for_controller()
        self.clock = pygame.time.Clock()

    # Creates the default data packet that is sent to main
    def pack_controller_values(self):
        values = {"rov_joysticks": self.rov_joysticks, "mani_joysticks": self.mani_joysticks,
                "rov_buttons": self.rov_buttons, "mani_buttons": self.mani_buttons, 
                "rov_dpad": self.rov_dpad, "mani_dpad": self.mani_dpad,
                "camera_to_control": self.camera_motor,
                "camera_movement": self.rov_joysticks[3] #Kan endres til annen akse!
                , "time_between_updates": self.duration}
        # print(values)
        return values
    # Says that button is no longer held in
    def reset_button(self, event) -> None:
        self.rov_buttons[event.button] = 0
        self.mani_buttons[event.button] = 0 

    
    def wait_for_controller(self):
        """wait_for_controller will attempt to connect until it finds a controller."""
        while True:   
            try:
                print("Attempting to Connect to controller")
                pygame.joystick.init()
                global rov_joystick
                global mani_joystick
                print(f"Found {pygame.joystick.get_count()}controllers.")
                #Kan legge til if statements for om = 1 eller = 2
                rov_joystick = pygame.joystick.Joystick(0)
                mani_joystick = pygame.joystick.Joystick(1)
                print(f"Connected to {rov_joystick.get_name()}")
                print(f"Connected to {mani_joystick.get_name()}")
                break
            except Exception as e:
                print(e)

        rov_joystick.init()
        mani_joystick.init()

    # Remaps a range. for example 1-10 range can be remapped to 1-100 so that for example 3 becomes 30
    def get_new_range(self, value, min, max, scale=100):
        return((value-min)/(max-min))*scale

    def normalize_joysticks(self, event):
        """Normalizes the joysticks between the desired values"""
        # (x-min)/(max-min)

        if event.axis == 1:
            return self.deadzone_adjustment(-round((2*(event.value--self.controller_stop_point)/(self.controller_stop_point--self.controller_stop_point)-1)*100))

        if event.axis == 3:
            return self.deadzone_adjustment(-round((2*(event.value--self.controller_stop_point)/(self.controller_stop_point--self.controller_stop_point)-1)*100))


        if event.axis == 4:
            return self.deadzone_adjustment(-round(self.get_new_range(event.value,-self.controller_stop_point, self.controller_stop_point))) # opp og ned på roboten har range fra 0 til 100 og 0 til -100
            # return round((event.value--self.controller_stop_point)/(self.controller_stop_point--self.controller_stop_point)*100)
        if event.axis == 5:
            return self.deadzone_adjustment(round(self.get_new_range(event.value,-self.controller_stop_point, self.controller_stop_point))) # opp og ned på roboten har range fra 0 til 100 og 0 til -100
            # return round((event.value--self.controller_stop_point)/(self.controller_stop_point--self.controller_stop_point)*100)

        return self.deadzone_adjustment(round((2*(event.value--self.controller_stop_point)/(self.controller_stop_point--self.controller_stop_point)-1)*100))

        # return round(self.get_new_range(event.value,-self.controller_stop_point, self.controller_stop_point))

    #Reset the controller if the value is below the set deadzone to prevent the stick from sending out values when it is let go and not properly reset
    def deadzone_adjustment(self, value) -> int:
        if abs(value) < self.joystick_deadzone+1:
            return 0
        return value

    #Used for writing which buttons are held in to the console
    def write_controller_values(self, local=False):
        # writestring = self.joysticks
        writestring = f"{self.buttons} - {self.dpad} - {self.joysticks}"
        if not local:
            return writestring
        
        # for i in range(len(self.joysticks)):
        #     writestring += f"axis {i} : {self.joysticks}%"
        sys.stdout.write("\r" + f"{writestring}                                     ")
        sys.stdout.flush()
        # sys.stdout.write("\r" + f"{self.buttons} - {self.joysticks}                     ")
        # sys.stdout.flush()

    # Test function that can make the controller vibrate.
    def lekkasje(self, duration=250, loops=3, pause_duration=500):
        for i in range(loops):
            rov_joystick.rumble(1,1,duration)
            time.sleep((duration+pause_duration)/1000)
    
    def get_events_loop(self, t_watch: Threadwatcher, id: int, debug=False, debug_all=False):
        """get_events_loop collects all the events and updates the buttons, dpad, and joystick values. It then sends it to the queue if it is not local"""
        while t_watch.should_run(id):
            if pygame.joystick.get_count() < 1:
                self.wait_for_controller()
            self.duration = self.clock.tick(20)
            # print(duration)
            for event in pygame.event.get():
                # print("entered event check")
                if event.type == DPAD: #dpad (both up and down)
                    self.dpad = event.value
                    # self.dpad = [val*100 for val in event.value]

                if event.type == BUTTON_DOWN: #button down
                    self.rov_buttons[event.button] = 1
                    self.mani_buttons[event.button] = 1

                    #Trenger sikkert ikke denne, skal nok bruke andre funksjoner !!!
                    if self.rov_buttons[BUTTON_Y] == 1:
                        self.camera_motor = (self.camera_motor+1)%2
                        # threading.Thread(target=self.lekkasje).start()

                    if debug_all:
                        if event.button == BUTTON_A:
                            print("A")
                        if event.button == BUTTON_B:
                            print("B")
                        if event.button == BUTTON_X:
                            print("X")
                        if event.button == BUTTON_Y:
                            print("Y")
                        if event.button == 4:
                            print("Left button")
                        if event.button == 5:
                            print("Right button")
                        if event.button == 6:
                            print("Back")
                        if event.button == 7:
                            print("Start")
                        if event.button == 8:
                            print("Thumb button left")
                        if event.button == 9:
                            print("Thumb button right")


                    # print(event.button)
                if event.type == BUTTON_UP: #button up
                    self.reset_button(event)

                    if debug_all:
                        if event.button == 0:
                            # pygame.joystick.Joystick.stop_rumble()
                            print("A up")
                        if event.button == 1:
                            print("B up")
                        if event.button == 2:
                            print("X up")
                        if event.button == 3:
                            print("Y up")
                        if event.button == 4:
                            print("Left button up")
                        if event.button == 5:
                            print("Right button up")
                        if event.button == 6:
                            print("Back up")
                        if event.button == 7:
                            print("Start up")
                        if event.button == 8:
                            print("Thumb button left up")
                        if event.button == 9:
                            print("Thumb button right up")
                    self.reset_button(event)

                # There is a bug where only one joystick is registered if the program has been started, but no buttons or dpad has been pressed yet.
                # this is "solved" by the fact that the other joystick reduces the value of the first joystick that was pressed. Since we add up the
                # joystick values to get total trust. Example: axis 4: -50, axis 5: 100. Value we get is 50. With bug: axis 4: 0, axis 5: 50.
                if event.type == JOYSTICK: #joystick movement
                    self.rov_joysticks[event.axis] = self.normalize_joysticks(event)
                    self.rov_joysticks[6] = self.rov_joysticks[4] + self.rov_joysticks[5]

                    self.mani_joysticks[event.axis] = self.normalize_joysticks(event)
                    self.mani_joysticks[6] = self.mani_joysticks[4] + self.mani_joysticks[5]

                    
                    if debug_all:
                        if event.axis == 0:
                            if event.value > 0:
                                print(f"Roboten kjører mot høyre med {self.normalize_joysticks(event)}% kraft")
                            else:
                                print(f"Roboten kjører mot venstre med {self.normalize_joysticks(event)}% kraft")
                        if event.axis == 4 or event.axis == 5:
                            print(f"{event.axis} signal: {event.value}, normalized: {self.normalize_joysticks(event)}")
                            if event.value > 0:
                                print(f"Roboten kjører framover med {self.normalize_joysticks(event)}% kraft")
                            else:
                                print(f"Roboten kjører bakover med {self.normalize_joysticks(event)}% kraft")
                        elif event.axis == 2:
                            if event.value > 0:
                                print(f"Roboten roterer mot klokka med {self.normalize_joysticks(event)}% kraft")
                            else:
                                print(f"Roboten roterer med klokka med {self.normalize_joysticks(event)}% kraft")
                        elif event.axis == 3:
                            if event.value > 0:
                                print(f"Roboten tilter kamera med {self.normalize_joysticks(event)}% kraft")
                            else:
                                print(f"Roboten tilter kamera med {self.normalize_joysticks(event)}% kraft")
                        elif event.axis == 4:
                                print(f"Roboten går ned med {self.normalize_joysticks(event)}% kraft")
                        elif event.axis == 5:
                                print(f"Roboten går opp med {self.normalize_joysticks(event)}% kraft")
            if self.queue_to_rov is not None: # Means we send the values to main
                self.queue_to_rov.put((1, self.pack_controller_values())) # 1 here is the id that tells main that this is from the controller and not a gui command or profile update
                # print(self.buttons)
            elif debug and self.connection is None: 
                self.write_controller_values(local=True)
        print("closed connection")
        # self.connection.close()            

# This is the entry point that main calls
def run(queue_to_rov, t_watch: Threadwatcher, id, debug=True, debug_all=False):
    debug_all = False
    c = Controller(queue_to_rov, t_watch, id)
    c.get_events_loop(t_watch, id, debug=debug, debug_all=debug_all)

if __name__ == "__main__":
    pass
    # c = Controller(None)
    # run(None, True, False)
    # c.get_events_loop(debug=True, debug_all=False)