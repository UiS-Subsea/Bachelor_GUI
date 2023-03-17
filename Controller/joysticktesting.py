import pygame

pygame.init()
joysticks={}
ROV = "030000005e040000ff02000000007200"
manipulator= "030000005e0400008e02000000007200"


for event in pygame.event.get():
    if event.type == pygame.JOYDEVICEADDED:
                    # This event will be generated when the program starts for every
                    # joystick, filling up the list without needing to create them manually.
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    
                    
                    #If the guid matches the ROV guid, then it is the ROV controller
                    if joy.get_guid() == ROV:
                        print("ROV controller is plugged in")
                    #If the guid matches the manipulator guid, then it is the manipulator controller
                    elif joy.get_guid() == manipulator:
                        print("Manipulator controller is plugged in")
                    else:
                        print("Unknown controller is plugged in")
