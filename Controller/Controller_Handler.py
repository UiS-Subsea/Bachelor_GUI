import sys
import time
import pygame
import multiprocessing
from Thread_info import Threadwatcher   #For full testing with main.py
# from Threadwatch import Threadwatcher   #For local testing on MAC
import threading
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
DPAD = 1538  # Kan ogs bruke pygame.JOYBUTTONDOWN hvis nødvendig
BUTTON_DOWN = 1539
BUTTON_UP = 1540
JOYSTICK = 1536

BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3

ROV_CONTROLLER_ID = 0
MANIPULATOR_CONTROLLER_ID = 1


def clear_screen():
    pass
    os.system("cls")


class Controller:
    def __init__(self, queue_to_rov: multiprocessing.Queue, manual_flag, t_watch: Threadwatcher, id, joystick_deadzone=15) -> None:
        # Queue that is received in main
        self.queue_to_rov = queue_to_rov
        # t_watch and id is used for closing the process from main
        self.t_watch = t_watch
        self.id = id
        # Variable that decides when we set the controller to be in the center. Used for stopping the controller sending small values when the stick is let go
        self.joystick_deadzone = joystick_deadzone  # deadzone in percent
        # list of all buttons that can be clicked. 1 means it is clicked and 0 is not clicked
        self.rov_buttons = [0]*15
        self.manual_flag = manual_flag
        self.mani_buttons = [0]*16
        # values for all axes of the joysticks (and one "virtual joystick" that combines axes)
        self.rov_joysticks = [0]*7

        self.mani_joysticks = [0]*7
        self.autonom_data = [0]*8
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
        self.button_names = {0: "A", 1: "B", 2: "X", 3: "Y",
                             7: "Left Joystick Press", 8: "Right Joystick Press",
                             9: "LB", 10: "RB",
                             11: "DPAD UP", 12: "DPAD DOWN", 13: "DPAD LEFT", 14: "DPAD RIGHT"}
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
                  "camera_to_control": self.camera_motor, "camera_movement": self.rov_joysticks[3], 
                  "autonomdata": self.autonom_data, "mani_dpad": self.mani_dpad, "rov_dpad": self.rov_dpad}
        # "camera_to_control": self.camera_motor,
        # "camera_movement": self.rov_joysticks[3] #Kan endres til annen akse!
        # , "time_between_updates": self.duration}
        # print(values)
        return values
    # Says that button is no longer held in

    def reset_button(self, event) -> None:
        self.rov_buttons[event.button] = 0
        self.mani_buttons[event.button] = 0
        # For å resette virtuell knapp 15 (index -11+12)
        self.mani_buttons[15] = 0

    def wait_for_controller(self):
        """wait_for_controller will attempt to connect until it finds a controller."""
        while True:
            try:
                global rov_joystick
                global mani_joystick
                pygame.joystick.init()
                if pygame.joystick.get_count() == 0:
                    raise Exception
                if pygame.joystick.get_count() == 1:
                    print(
                        f"Found {pygame.joystick.get_count()} controller. Connecting to ROV Only!")
                    rov_joystick = pygame.joystick.Joystick(0)
                    print(f"Connected to {rov_joystick.get_name()}")
                if pygame.joystick.get_count() == 2:
                    print(
                        f"Found {pygame.joystick.get_count()} controllers. Connecting BOTH!")
                    rov_joystick = pygame.joystick.Joystick(0)
                    mani_joystick = pygame.joystick.Joystick(1)
                    print(f"Connected to {rov_joystick.get_name()}")
                    print(f"Connected to {mani_joystick.get_name()}")
                break
            except Exception as e:
                print(e)
                for sec in range(5, 0, -1):
                    sys.stdout.write(
                        "\r" + f"Shut down and connect controller/s before starting! {sec}")
                    time.sleep(1)
                    sys.stdout.flush()
        if pygame.joystick.get_count() == 1:
            rov_joystick.init()
        elif pygame.joystick.get_count() == 2:
            rov_joystick.init()
            mani_joystick.init()
            # Indicates which controller that controls the ROV
            rov_joystick.rumble(0.1, 0, 100)

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

        if event.axis == 2:
            # opp og ned på roboten har range fra 0 til 100 og 0 til -100
            return self.deadzone_adjustment(round(self.get_new_range(event.value, -self.controller_stop_point, self.controller_stop_point)))
            # return round((event.value--self.controller_stop_point)/(self.controller_stop_point--self.controller_stop_point)*100)
        if event.axis == 5:
            # opp og ned på roboten har range fra 0 til 100 og 0 til -100
            return self.deadzone_adjustment(round(self.get_new_range(event.value, -self.controller_stop_point, self.controller_stop_point)))
            # return round((event.value--self.controller_stop_point)/(self.controller_stop_point--self.controller_stop_point)*100)
            
        if event.axis == 2:
            # opp og ned på roboten har range fra 0 til 100 og 0 til -100
            return self.deadzone_adjustment(round(self.get_new_range(event.value, -self.controller_stop_point, self.controller_stop_point)))
            # return round((event.value--self.controller_stop_point)/(self.controller_stop_point--self.controller_stop_point)*100)

        return self.deadzone_adjustment(round((2*(event.value--self.controller_stop_point)/(self.controller_stop_point--self.controller_stop_point)-1)*100))

        # return round(self.get_new_range(event.value,-self.controller_stop_point, self.controller_stop_point))

    # Reset the controller if the value is below the set deadzone to prevent the stick from sending out values when it is let go and not properly reset
    def deadzone_adjustment(self, value) -> int:
        if abs(value) < self.joystick_deadzone+1:
            return 0
        return value

    # Used for writing which buttons are held in to the console
    def write_controller_values(self, local=False):
        # writestring = self.joysticks
        writestring = f"{self.buttons} - {self.dpad} - {self.joysticks}"
        if not local:
            return writestring

        # for i in range(len(self.joysticks)):
        #     writestring += f"axis {i} : {self.joysticks}%"
        sys.stdout.write(
            "\r" + f"{writestring}                                     ")
        sys.stdout.flush()
        # sys.stdout.write("\r" + f"{self.buttons} - {self.joysticks}                     ")
        # sys.stdout.flush()

    # Test function that can make the controller vibrate.
    def lekkasje(self, duration=250, loops=3, pause_duration=500):
        for i in range(loops):
            rov_joystick.rumble(1, 1, duration)
            time.sleep((duration+pause_duration)/1000)

    def get_events_loop(self, t_watch: Threadwatcher, id: int, debug=False, debug_all=False):
        """get_events_loop collects all the events and updates the buttons, dpad, and joystick values. It then sends it to the queue if it is not local"""
        while t_watch.should_run(id):
            if pygame.joystick.get_count() < 1:
                self.wait_for_controller()
            #tickrate
            ### ENDRE TICK TIL 20 FOR NORMAL KJØRING
            ### ENDRE TIL MINDRE FOR Å DEBUGGE LETTERE
            self.duration = self.clock.tick(20)
            
            # print(duration)
            for event in pygame.event.get():
                self.manual_flag.value = 1
                if event.type == DPAD: #dpad (both up and down)
                    if event.joy == ROV_CONTROLLER_ID:
                        self.rov_dpad = event.value # BLIR DET BRUKT ELLER ER DET KNAPP?
                    if event.joy == MANIPULATOR_CONTROLLER_ID:
                        self.mani_dpad = event.value # BLIR DET BRUKT ELLER ER DET KNAPP?
                    # self.dpad = [val*100 for val in event.value]

                if event.type == BUTTON_DOWN:  # button down
                    if event.joy == ROV_CONTROLLER_ID:
                        self.rov_buttons[event.button] = 1
                    elif event.joy == MANIPULATOR_CONTROLLER_ID:
                        self.mani_buttons[event.button] = 1
                        # Virtual button for mapping -1 to 1 on arm forward / backward
                        self.mani_buttons[15] = (
                            (-self.mani_buttons[12]) + self.mani_buttons[11])

                    # Trenger sikkert ikke denne, skal nok bruke andre funksjoner !!!
                    if self.rov_buttons[BUTTON_Y] == 1:
                        self.camera_motor = (self.camera_motor+1) % 2
                        # threading.Thread(target=self.lekkasje).start()

                    if debug_all:
                        if event.joy == ROV_CONTROLLER_ID:
                            if event.button == BUTTON_A:
                                print("ROV: A")
                            elif event.button == BUTTON_B:
                                print("ROV: B")
                            elif event.button == BUTTON_X:
                                print("ROV: X")
                            elif event.button == BUTTON_Y:
                                print("ROV: Y")
                            elif event.button == 7:
                                print("ROV: Left Joystick Press")
                            elif event.button == 8:
                                print("ROV: Right Joystick Press")
                            elif event.button == 9:
                                print("ROV: LB")
                            elif event.button == 10:
                                print("ROV: RB")
                            elif event.button == 11:
                                print("ROV: DPAD - Up")
                            elif event.button == 12:
                                print("ROV: DPAD - Down")
                            elif event.button == 13:
                                print("ROV: DPAD - Left")
                            elif event.button == 14:
                                print("ROV: DPAD - Right")
                        if event.joy == MANIPULATOR_CONTROLLER_ID:
                            if event.button == BUTTON_A:
                                print("MANIPULATOR: A")
                            elif event.button == BUTTON_B:
                                print("MANIPULATOR: B")
                            elif event.button == BUTTON_X:
                                print("MANIPULATOR: X")
                            elif event.button == BUTTON_Y:
                                print("MANIPULATOR: Y")
                            elif event.button == 7:
                                print("MANIPULATOR: Left Joystick Press")
                            elif event.button == 8:
                                print("MANIPULATOR: Right Joystick Press")
                            elif event.button == 9:
                                print("MANIPULATOR: LB")
                            elif event.button == 10:
                                print("MANIPULATOR: RB")
                            elif event.button == 11:
                                print("MANIPULATOR: DPAD - Up")
                            elif event.button == 12:
                                print("MANIPULATOR: DPAD - Down")
                            elif event.button == 13:
                                print("MANIPULATOR: DPAD - Left")
                            elif event.button == 14:
                                print("MANIPULATOR: DPAD - Right")

                    # print(event.button)
                if event.type == BUTTON_UP:  # button up
                    self.reset_button(event)

                    if debug_all:
                        if event.button == 0:
                            print("A up")
                        if event.button == 1:
                            print("B up")
                        if event.button == 2:
                            print("X up")
                        if event.button == 3:
                            print("Y up")
                        if event.button == 7:
                            print("Left Joystick Press UP")
                        if event.button == 8:
                            print("Right Joystick Press UP")
                        if event.button == 9:
                            print("LB UP")
                        if event.button == 10:
                            print("RB UP")
                        if event.button == 11:
                            print("DPAD - Up UP")
                        if event.button == 12:
                            print("DPAD - Down UP")
                        if event.button == 13:
                            print("DPAD - Left UP")
                        if event.button == 14:
                            print("DPAD - Right UP")
                    # self.reset_button(event)

                # There is a bug where only one joystick is registered if the program has been started, but no buttons or dpad has been pressed yet.
                # this is "solved" by the fact that the other joystick reduces the value of the first joystick that was pressed. Since we add up the
                # joystick values to get total trust. Example: axis 4: -50, axis 5: 100. Value we get is 50. With bug: axis 4: 0, axis 5: 50.
                if event.type == JOYSTICK:  # joystick movement JOYSTICK
                    if event.joy == ROV_CONTROLLER_ID: # LT = 2, RT = 5
                        self.rov_joysticks[event.axis] = self.normalize_joysticks(
                            event)
                        # print(f"{event.axis}: {event.value}")
                        self.rov_joysticks[6] = self.rov_joysticks[5] - self.rov_joysticks[2]
                        # self.rov_joysticks[6] = (1+self.rov_joysticks[5])/2 - \
                        #     (1-self.rov_joysticks[2])/2
                    elif event.joy == MANIPULATOR_CONTROLLER_ID:
                        self.mani_joysticks[event.axis] = self.normalize_joysticks(
                            event)
                        # self.mani_joysticks[6] = self.mani_joysticks[2] + \
                        #     self.mani_joysticks[5]
                        self.mani_joysticks[6] = self.mani_joysticks[5] - self.mani_joysticks[2]

                    if debug_all:
                        deadzone = 0.07  # To prevent sensitive output in console
                        if event.joy == ROV_CONTROLLER_ID:
                            if event.axis == 0:
                                print(event.axis)
                                if event.value > deadzone:
                                    print(
                                        f"ROV til HØYRE med {self.normalize_joysticks(event)}% kraft")
                                elif event.value < -deadzone:
                                    print(
                                        f"ROV til VENSTRE med {self.normalize_joysticks(event)}% kraft")
                            if event.axis == 4 or event.axis == 5:
                                print(
                                    f"Axis: {event.axis}. signal: {event.value}, normalized: {self.normalize_joysticks(event)}")
                            if event.axis == 1:
                                print(event.axis)
                                if event.value > deadzone:
                                    print(
                                        f"ROV BAKOVER med {self.normalize_joysticks(event)}% kraft")
                                elif event.value < -deadzone:
                                    print(
                                        f"ROV FREMOVER med {self.normalize_joysticks(event)}% kraft")
                            elif event.axis == 2:
                                print(event.axis)
                                if event.value > deadzone:
                                    print(
                                        f"ROV roterer MED klokka med {self.normalize_joysticks(event)}% kraft")
                                elif event.value < -deadzone:
                                    print(
                                        f"ROV roterer MOT klokka med {self.normalize_joysticks(event)}% kraft")
                            elif event.axis == 3:
                                print(event.axis)
                                if event.value > deadzone:
                                    print(
                                        f"ROV tilter kamera med {self.normalize_joysticks(event)}% kraft")
                                elif event.value < -deadzone:
                                    print(
                                        f"ROV tilter kamera med {self.normalize_joysticks(event)}% kraft")
                            elif event.axis == 4:
                                print(event.axis)
                                print(
                                    f"ROV NEDOVER med {self.normalize_joysticks(event)}% kraft")
                            elif event.axis == 5:
                                print(event.axis)
                                print(
                                    f"ROV OPPOVER med {self.normalize_joysticks(event)}% kraft")
                        elif event.joy == MANIPULATOR_CONTROLLER_ID:
                            if event.axis == 0:
                                if event.value > deadzone:
                                    print(
                                        f"MANIPULATOR til HØYRE med {self.normalize_joysticks(event)}% kraft")
                                elif event.value < -deadzone:
                                    print(
                                        f"MANIPULATOR til VENSTRE med {self.normalize_joysticks(event)}% kraft")
                            if event.axis == 4 or event.axis == 5:
                                print(
                                    f"{event.axis} signal: {event.value}, normalized: {self.normalize_joysticks(event)}")
                            if event.axis == 1:
                                if event.value > deadzone:
                                    print(
                                        f"MANIPULATOR BAKOVER med {self.normalize_joysticks(event)}% kraft")
                                elif event.value < -deadzone:
                                    print(
                                        f"MANIPULATOR FREMOVER med {self.normalize_joysticks(event)}% kraft")
                            elif event.axis == 2:
                                if event.value > deadzone:
                                    print(
                                        f"MANIPULATOR roterer MED klokka med {self.normalize_joysticks(event)}% kraft")
                                elif event.value < -deadzone:
                                    print(
                                        f"MANIPULATOR roterer MOT klokka med {self.normalize_joysticks(event)}% kraft")
                            elif event.axis == 3:
                                if event.value > deadzone:
                                    print(
                                        f"MANIPULATOR tilter kamera med {self.normalize_joysticks(event)}% kraft")
                                elif event.value < -deadzone:
                                    print(
                                        f"MANIPULATOR tilter kamera med {self.normalize_joysticks(event)}% kraft")
                            elif event.axis == 4:
                                print(
                                    f"MANIPULATOR NEDOVER med {self.normalize_joysticks(event)}% kraft")
                            elif event.axis == 5:
                                print(
                                    f"MANIPULATOR OPPOVER med {self.normalize_joysticks(event)}% kraft")
            if self.queue_to_rov is not None:  # Means we send the values to main
                # 1 here is the id that tells main that this is from the controller and not a gui command or profile update
                self.queue_to_rov.put((1, self.pack_controller_values()))
                # print(self.buttons)
                
                # What the thing being sent into queue looks like:
                # (1, {"rov_joysticks": [], "mani_joysticks": [], "buttons": []})
                
            elif debug and self.connection is None:
                self.write_controller_values(local=True)
        print("closed connection")
        # self.connection.close()

# This is the entry point that main calls
def run(queue_to_rov,manual_flag, t_watch: Threadwatcher, id, debug=True, debug_all=True):
    # debug_all = True
    c = Controller(queue_to_rov, manual_flag, t_watch, id)
    c.get_events_loop(t_watch, id, debug=debug, debug_all=debug_all)


if __name__ == "__main__":
    pass

    # queue = multiprocessing.Queue()
    # t_watch = Threadwatcher()
    # id = t_watch.add_thread()
    # c = Controller(queue, t_watch, id)
    # c.get_events_loop(t_watch, id,debug=True, debug_all=False)
