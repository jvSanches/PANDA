from time import sleep
from panda_board import panda
import msvcrt

myPanda = panda('auto')
input("Hit enter to start")
print("Press esc to stop")

while 1:
    myPanda.setLed(1)
    sleep(0.25)
    myPanda.setLed(0)
    sleep(0.25)

    # body of the loop ...
    if msvcrt.kbhit():
        if ord(msvcrt.getch()) == 27:
            break



myPanda.disconnect()

