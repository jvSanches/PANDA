#----------------------------------------------------------------------

# Software da PANDA
# TCC - Engenharia Mecatrônica - Poli USP
# Guilherme de Agrela Lopes
# João Vitor Sanches
#
# PANDA DEMO APPLICATION
#
# Uses the classes on panda_board:
# panda is used to communicate with the board
# monitor is a easy to use real time grapher
# See instructions bellow
#----------------------------------------------------------------------
from panda_board import panda, monitor
import msvcrt


#Instancing of a Panda 
myPanda=panda('auto')

#Set led frequiency to 15Hz
myPanda.setLedFreq(15)

# Declaration of a getter function to read the voltage at Analog in 1
def voltage():
    return 3.3/4096 * myPanda.getAnalog1() #Calculation to map the 12bit adc value to a 0V~3.3V range

# Decalration of another getter function, independent from the board. It generates a sawtooth wave
count_val = 0
def st_wave():
    global count_val
    count_val += 0.1
    if count_val > 3.3:
        count_val = 0
    return count_val   


#Instancing of a monitor with sampling time and number of samples to be shown at once
g = monitor(0.1, 50)

#Assign a curve to represent the voltage value. Note the first argument is a legend and the second is a FUNCTION 
g.addCurve('AIN1 Voltage', voltage)

# Same. Again, be sure no to pass the second argument as _function()_
g.addCurve('Sawtooth', st_wave)

#Led will start blinking at 15 Hz
myPanda.setLedMode("BLINK")

#The monitor will pop-up
g.start()
print("Press esc on the console to stop")
while 1:
    #Keeps updating the graph
    g.update()

    #Until user presses ESC on the console    
    if msvcrt.kbhit():
        if ord(msvcrt.getch()) == 27:
            break

myPanda.setLedMode("OFF")
# Disconnects
myPanda.disconnect()