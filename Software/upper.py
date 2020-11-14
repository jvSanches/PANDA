from time import sleep
from panda_board import panda
import msvcrt

myPanda = panda('auto')
input("Hit enter to start")
print("Press esc to stop")

while 1:
    myPanda.setLedMode(1)
    print(myPanda.getAnalog1()) 
    sleep(0.1)
    myPanda.setLedMode(0)
    print(myPanda.getAnalog1())
    sleep(0.1)

    # body of the loop ...
    if msvcrt.kbhit():
        if ord(msvcrt.getch()) == 27:
            break



myPanda.disconnect()

