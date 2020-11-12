import serial
import serial.tools.list_ports
from time import sleep
from datetime import datetime
DEVICE_INQUIRE_TIMEOUT = 0.5

def getPandaPorts():
    ports = [str(i).split()[0] for i in serial.tools.list_ports.comports()]
    pandas = []
    for portname in ports:
        device = serial.Serial(portname)
        sleep(0.5)
        device.write([35, 1, 1, 13, 10])
        sleep(0.1)
        answer = []
        scanstart = datetime.now()
        timeout = 0        
        while device.in_waiting > 0 and not timeout:
            timeout = (datetime.now() - scanstart).total_seconds() > DEVICE_INQUIRE_TIMEOUT
            answer = (device.read(device.in_waiting))
        if(answer):            
            pandas.append(portname)            
        device.close()
    return pandas


class panda:
    def __init__(self, port, id = None):
        if port == 'auto':
            available_pandas = getPandaPorts()
            if available_pandas:
                self.board = serial.Serial(available_pandas[0])
                self.board.write([35, 2, 10, 2, 13, 10])
                self.board.write([35, 2, 12, 20, 13, 10])
                sleep(0.5)
                self.board.write([35, 2, 10, 0, 13, 10])
                
    def disconnect(self):
        self.board.close()
