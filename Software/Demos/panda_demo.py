'''
Panda Demo

This program initializes a panda object (connects to the board) and continuously
requests the value from Analog In 1 (ranging from 0 to 4096). The main loop also 
keeps toggling the board LED.
After a succesful connection the user will be prompted to press any key to start 
the loop.
By pressing the ESC key, the loop stops and the board is disconnected.
'''

from time import sleep
from panda_board import panda
import msvcrt

myPanda = panda('auto') # A serial port can be especified. "auto" makes everything easier

print("Press esc to stop \n")
input("Hit Any key to start")

while 1:
    myPanda.setLedMode("ON") #Mode 1 = ON
    print(myPanda.getAnalog1()) 
    sleep(0.5)
    myPanda.setLedMode(0)#Mode 0 = "OFF"
    print(myPanda.getAnalog1())
    sleep(0.5)

    # Scans for esc keypress
    if msvcrt.kbhit():
        if ord(msvcrt.getch()) == 27:
            break



myPanda.disconnect()

