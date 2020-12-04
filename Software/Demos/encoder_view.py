from panda_board import panda
import msvcrt
from time import sleep

myPanda = panda('auto')

def encoderTurns():
    ticks_per_rev = 40
    ticks = myPanda.getEncoderCount()
    if ticks > 2147483648:
        ticks -= 4294967296
    return ticks#/ticks_per_rev
while 1:
    #Keeps updating the graph
    print(myPanda.getEncoderCount())
    sleep(0.5)

    #Until user presses ESC on the console    
    if msvcrt.kbhit():
        k = ord(msvcrt.getch())
        if  k == 27:
            print("Stopping")            
            break
        if  k == 122:
            myPanda.setEncoderCount(0)            
            

# Disconnects
myPanda.disconnect()