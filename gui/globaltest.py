import threading
import time
from globaltest2 import *


def controller():
    while True:
        print("From Controller")
        toggle()
        print("Controller!")
        time.sleep(1)
        
def autonomous():
    while True:
        print("From Autonomous")
        toggle()
        print("Autonomous!")
        time.sleep(1)
        

if __name__ == "__main__":
    
    threading.Thread(target=controller).start()
    threading.Thread(target=autonomous).start()