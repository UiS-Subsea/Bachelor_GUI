import os
import pygame
import time
import sys
import multiprocessing


class Controller:
    def __init__(self,joystick_deadzone=15)->None:
        self.joystick_deadzone = joystick_deadzone #in %
        #List of buttons
        self.buttons=[0]*10
        #List of joysticks axis (and one virtual joystick that combines the two axis)
        self.joysticks = [0]*7
        #tuple for dpad controll. Goes from -1 to 1 on both first and second variable
        