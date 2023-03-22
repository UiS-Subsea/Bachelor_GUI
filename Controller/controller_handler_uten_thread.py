import multiprocessing
import sys
import time
import pygame

import os
#Hides "Hello from pygame community" when running
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

### Variable names for numbers equal to their description ###
DPAD = 1538
BUTTON_DOWN = 1539
BUTTON_UP = 1540
JOYSTICK = 1536

BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3


#have not used Threadwatcher from last year, dont think we need "id" then either
class Controller:
    def __init__(self, queue_to_rov: multiprocessing.Queue, joystick_deadzone=15) -> None:
        #Queue that is recieved in main
        self.queue_to_rov = queue_to_rov
        self.id = id
        #Variable that stops the controller from sending small values when the stick is idle
        self.joystick_deadzone = joystick_deadzone
        #List of all clickable buttons. 1=clicked, 0= not clicked
        self.buttons = [0]*10
        #values of axis on joystick (+ one virtual)
        self.joysticks = [0]*7
        #tuple for dpad control. Goes from -1 to 1 on both first and second variable
        self.dpad = (0,0)
        #controller stop point can be used to normalize the max value on controller to 1
        self.controller_stop_point = 1.04     #1.000030518509476 
        self.camera_motor = 0
        #Variable used if controller needs to reset before trying to connect. First run does not need reset
        self.first_run = True
        #Map of names of buttons in self.buttons list
        self.button_names = {0:"A", 1:"B", 2:"X", 3:"Y", 4:"Left Button Back", 
                             5:"Right Button Back", 6:"Back", 7:"Start", 
                             8:"Thumb Button Left", 9:"Thumb Button Right"}
        #Initialize the duration timer which says how long since last time the .tick method was called
        self.duration = -1
        pygame.init()
        #Waits for controller to be found and tries to connect to it
        self.wait_for_controller()
        self.clock = pygame.time.Clock()

    def pack_controller_values(self):
        values = {"joysticks": self.joysticks, "camera_movement": self.joysticks[3], 
                  "buttons": self.buttons, "dpad": self.dpad, 
                  "camera_to_control": self.camera_motor, "time_between_updates": self.duration}
        return values
    
    #Says that button is no longer held in
    def reset_button(self, event) -> None:
        self.buttons[event.button] = 0

    def wait_for_controller(self):
        """wait_for_controller will attempt to connect until it finds a controller."""
        # while self.t_watch.should_run(self.id) was before
        #Now we only use bool True (can make a variable)
        while True:    
            try:
                if not self.first_run: #if not True since first_run = True
                    #?Opposite of init(), so it resets
                    pygame.joystick.quit()
                else:
                    print("Attempting to Connect to controller")
                pygame.joystick.init()
                global joystick

                # HERE WE CAN ADD FUNCTIONALITY OF MULTIPLE CONTROLLERS!

                if pygame.joystick.get_count() > 1:
                    print("Found several controllers. Connecting to controller 0 only")
                joystick = pygame.joystick.Joystick(0)
                print(f"Connected to {joystick.get_name()}")
                break
            except:
                self.first_run = False
                for sec in range(5,0,-1):
                        sys.stdout.write("\r" + f"Could not find controller. If it is already connected, try reconnecting it! Retrying in {sec} seconds")
                        time.sleep(1)
                        sys.stdout.flush()
        #If everything above is done or not needed, initialize joystick
        joystick.init()

    def get_new_range(self, value, min, max, scale=100):
        return ((value-min)/(max-min)*scale)
    
    #Resets controller if value is less than deadzone to prevent unwanted values sent out if not properly reset
    def deadzone_adjustment(self, value) -> int:
        if abs(value) < self.joystick_deadzone+1:
            return 0
        return value
    
    def normalize_joysticks(self, event):
        """Normalized the joysticks between the desired values """
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
    
    #For writing which buttons are held in console
    def write_controller_values(self, local=False):
        writestring = f"{self.buttons} - {self.dpad} - {self.joysticks}"
        if not local:
            return writestring
        sys.stdout.write("\r", f"{writestring}")
        sys.stdout.flush()

    #Can change debugs to see console reports of things like button presses
    def get_events_loop(self, debug=False, debug_all=False):

        #can add variable to change True in different way

        while True:
            #Checks if any controllers are detected, if not, call wait_for_controller()
            if pygame.joystick.get_count() < 1:
                self.wait_for_controller()
            #20HZ -> 20 ticks
            self.duration = self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == DPAD: #dpad both up and down
                    self.dpad = event.value

                if event.type ==BUTTON_DOWN: #Button Down /Press
                    self.buttons[event.button] = 1

                    if self.buttons[BUTTON_Y] == 1: #Button Y Pressed Down
                        #Effectively returns 0 or 1, depending on the current value of the variable
                        #If camera_motor = 1, then 1+1 modulo 2 equals 0
                        #If camera_motor = 0, then 0+1 modulo 2 equals 1
                        self.camera_motor = (self.camera_motor+1)%2
                    
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

                if event.type == BUTTON_UP:
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

                ## MIGHT BE ABLE TO FIX BUG FROM LAST YEAR
                ## BUT FOR NOW WE COPY

                if event.type == JOYSTICK: #joystick movement
                    self.joysticks[event.axis] = self.normalize_joysticks(event)
                    self.joysticks[6] = self.joysticks[4] + self.joysticks[5]

                    # Displays what the axis on joystick represents in console
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
                # if self.queue_to_rov is not None: #Means we send values to main (not None=Har data?)
                    #1 represents id that tells main that this data is from the controller
                    # self.queue_to_rov.put(1, self.pack_controller_values())

                ### Connection ? ### Spør Vebjørn !

                # if debug and self.connection is None:
                    # self.write_controller_values(local=True)
            # print("closed connection")

# Entry point that main.py calls
def run(queue_to_rov, debug=True, debug_all=False):
    # debug_all = False
    c = Controller(queue_to_rov)
    c.get_events_loop(debug=debug, debug_all=debug_all)

def test_controller_output():
    queue = multiprocessing.Queue()
    controller = Controller(queue_to_rov=queue)
    while True:
        # This is just to see the output
        print(controller.pack_controller_values())
        # Let's stop the test after one output
        if pygame.time.get_ticks() > 50:
            break
        # Sleep for a bit before the next update
        time.sleep(0.1)
    
if __name__ == "__main__":
    # pass
    test_controller_output()
    queue = multiprocessing.Queue()
    #Runs run() with debug_all = true
    run(queue, False, True)
    