'''
Panda scale Demo

This program initializes a panda object (connects to the board) and continuously
requests the value from the amplifier (ranging from 0 to 4096). The main loop also 
keeps toggling the board LED.
After a succesful connection the user will be prompted to press any key to start 
the loop.
By pressing the ESC key, the loop stops and the board is disconnected.
'''

from time import sleep
from panda_board import panda
import msvcrt

#Constant to be used as converting factor from 12bit adc value to a weight measurement
Km = -0.7070365358592695 # g/bit
Gain = 600

myPanda = panda('auto') # A serial port can be especified. "auto" makes everything easier

print("Press ESC to stop, Z to zero or C to calibrate \n")
input("Hit Enter key to start")

myPanda.setGain(Gain)
myPanda.setLedMode("ON") #Mode 1 = ON
samples = 10
while 1:
    digital_value = 0
    for i in range(samples):
        digital_value += myPanda.getAmpValue()
    digital_value /= samples
    weight = (digital_value - 2048) * Km # corrects mid scale offset and apllies the linear factor
    print("Weight measurement: %.1f g" %(weight)) 
    sleep(0.1)

    # Scans for keypress
    if msvcrt.kbhit():
        key = ord(msvcrt.getch())
        if key == 27: # ESC
            break #Stops the program
        elif key == 122: # Z Key
            print("Zeroing the device")
            myPanda.runAutoOffset() #Hardware offset performed by the board

        elif key == 99: #C Key
            known_value = int(input("Enter the known value: "))
            if known_value != None:
                Km = known_value / (digital_value-2048)
                print("New Km is: ", Km)

myPanda.setLedMode("OFF") #Mode 0 = OFF

myPanda.disconnect()