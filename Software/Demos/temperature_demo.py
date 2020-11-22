#----------------------------------------------------------------------

# Software da PANDA
# TCC - Engenharia Mecatrônica - Poli USP
# Guilherme de Agrela Lopes
# João Vitor Sanches
#
# PANDA THERMICS APPLICATION
#
# This example reads load cell data, temperature (2 channels) and rotationn, 
# according to the needs of a steam engine testing activity
# Data is displayed with the monitor Class and some logging is made to a csv file
# 
# Each of the 10k NTC thermistor should be connect to Vref and it's AIN. User must 
# verify the board has resistors soldered to R9 and R12 (they are near User Analog 
# connector and are soldered by default upon board assembly)
#----------------------------------------------------------------------
from panda_board import panda, monitor
import msvcrt
from datetime import datetime
from math import log
from time import sleep


#Instancing of a Panda 
myPanda=panda('auto')

#Set led frequiency to 15Hz
myPanda.setLedFreq(15)

# Configure amplifier gain to 500
myPanda.setGain(500)
sleep(1)

myPanda.runAutoOffset()

# Declaration of a getter function to read the voltage at Analog in 1
def voltage():
    return 3.3/4096 * (myPanda.getAmpValue()-2048) #Calculation to map the 12bit adc value to a 0V~3.3V range

# Function to calculate the torque
def torque():
    Kt = -100 # mNm/V     Depends on the load cell and gain used
    return voltage()*Kt


# Declaration of a getter function to read the number of turns in the encoder
def encoderTurns():
    ticks_per_rev = 40
    ticks = myPanda.getEncoderCount()
    if ticks > 2147483648: #Zero offset for the  32bit count
        ticks -= 4294967296
    return ticks/ticks_per_rev

#Variables to keep values between function calls
last_encoder_pos = 0 
last_encoder_time = datetime.now()
# Getter function to calculate angular speed in rpm
def angSpeed():
    global last_encoder_pos
    global last_encoder_time
    delta_time = (datetime.now() - last_encoder_time).total_seconds()
    last_encoder_time = datetime.now()
    delta_ang = encoderTurns() - last_encoder_pos
    last_encoder_pos = encoderTurns()
    return (delta_ang/delta_time)

# Returns the temperature in Kelvins, calulated from ADC value with Steinhart–Hart equation
# https://en.wikipedia.org/wiki/Steinhart%E2%80%93Hart_equation
# The voltage measured by the adc is Vadc = Vref * Rthermistor / (Rthermistor + 10 KOhm), and Vadc = (adc_value / 4096) * Vref
# thus, Rthermistor = ((10KOhm * Vadc) - Vref ) / (1 - Vadc)
def calc_temp(adc_value):
    a = 1.009249522e-03
    b = 2.378405444e-04
    c = 2.019202697e-07
    Vref = 3.3
    Vadc = (adc_value/4096) * Vref
    Rt = ((10000 * Vadc) - Vref ) / (1 - Vadc)
    ##Rt = 10000   # Unncoment to avoid errors while testing. Keeps output at 25 deg.C
    Temp_K = (1.0 / (a + b*log(Rt) + c*log(Rt)**3))
    return Temp_K-273

#Getter functions to be passed to the monitor 
def temp1():
    return calc_temp(myPanda.getAnalog1())
def temp2():
    return calc_temp(myPanda.getAnalog2())

#Instancing of a monitor with sampling time and number of samples to be shown at once
g = monitor(0.1, y_label='Values')

#Assign curves to the monitor. The curves will share the Y axis, watch out for the best unitis to get a better visualization
g.addCurve('Temperature 1 [deg. c]', temp1)
g.addCurve('Temperature 2 [deg. c]', temp2)

g.addCurve('Speed [rps]', angSpeed)

g.addCurve('Torque [mNm]', torque)

#Led will start blinking at 15 Hz
myPanda.setLedMode("BLINK")

#The monitor will pop-up
g.start()
print("Press ESC to stop or Space to pause")
while 1:
    #Keeps updating the graph
    g.update()

    #Until user presses ESC on the console    
    if msvcrt.kbhit():
        k = ord(msvcrt.getch())
        if  k == 27:
            print("Stopping")
            
            break
        elif k == 32:
            g.stop()
            input("Press Enter to resume...")
            myPanda.setLedMode("OFF")
            g.resume()
            print("Press ESC to stop or Space to pause")
            myPanda.setLedMode("BLINK")
        else:
            print("Press ESC to stop or Space to pause")

myPanda.setLedMode("OFF")
# Disconnects
myPanda.disconnect()