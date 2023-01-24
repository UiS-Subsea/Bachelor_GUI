import pygame
from pygame.locals import *

pygame.init()
joystick=pygame.joystick

if pygame.joystick.init():
    print("Connected to Joystick")
else:
    print("Something went wrong try restarting the program")
    





while True:
    for event in pygame.event.get(): # get the events (update the joystick)
        if event.type == QUIT: # allow to click on the X button to close the window
            pygame.quit()
            exit()

    
    if joystick.get_button(0):
        print("stopped")
        break
    

