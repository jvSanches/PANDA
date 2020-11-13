import serial
import serial.tools.list_ports
import struct
from time import sleep
from datetime import datetime
DEVICE_INQUIRE_TIMEOUT = 0.5

def getPandaPorts():
    ports = [str(i).split()[0] for i in serial.tools.list_ports.comports()]
    pandas = []
    for portname in ports:
        try:
            device = serial.Serial(portname, baudrate = 57600)
            sleep(0.5)
            device.write([35, 1, 1, 13, 10])
            sleep(0.1)
            answer = []
            scanstart = datetime.now()
            timeout = 0        
            while device.in_waiting > 0 and not timeout:
                timeout = (datetime.now() - scanstart).total_seconds() > DEVICE_INQUIRE_TIMEOUT
                answer = (device.read(device.in_waiting))
            if(b'I am a Panda' in answer):            
                pandas.append(portname)      
                    
            device.close()
        except:
            pass
    return pandas


class panda:
    def send(self, data):
        if (self.board):
            le = len(data)
            msg  =[35, le] + data + [13, 10]
            self.board.write(msg)
            print("sent: ", [i for i in msg])
        else:
            print("Serial port not Configured")
    def receive(self):
        lines = []
        
        while self.board.in_waiting > 0:
            lines.append(self.board.readline())
        if lines:
            if len(lines) > 1:
                print("Unexpected lines received")
            print("Received: ", [i for i in lines[-1]])
            return lines[-1]
        else:
            return 0

    def waitAck(self, timeout = 0.1):
        wait_start = datetime.now()
        _timeout = 0
        while self.board.in_waiting == 0 and not _timeout:
                _timeout = (datetime.now() - wait_start).total_seconds() > timeout
                
        msg = self.receive() 
        if msg:
            return msg
        else:
            print("Panda didn't answered last call")
            return 0

    def __init__(self, port, id = None):
        if port == 'auto':
            available_pandas = getPandaPorts()
            self.board = 0
            if available_pandas:
                self.board = serial.Serial(available_pandas[0], baudrate = 57600, timeout = 0.2)
                self.send([10, 2])
                self.waitAck()
                self.send([12, 20])
                self.waitAck()
                self.send([5, 1])
                self.waitAck()
                sleep(0.5)
                self.send([10, 0])
                self.waitAck()
                print("Panda Connected")
                
            else:
                print("No pandas available...")
                
    def disconnect(self):
        if self.board:
            self.send([5, 0])
            self.waitAck()
            self.send([10, 2])
            self.waitAck()
            self.send([12, 20])
            self.waitAck()
            sleep(0.5)
            self.send([10, 0])
            self.waitAck()
            self.board.close()
            print("Panda Disconnected")
        
    def setLedMode(self, state):
        if state == "OFF" or state == 0:
            self.send([10,0])
        elif state == "ON" or state == 1:
            self.send([10,1])
        elif state == "BLINK" or state == 2:
            self.send([10,2])        
        return bool(self.waitAck())

    def setLedFreq(self, freq):
        if freq > 100 or freq < 1:
            print("Frequency out of bounds")
            return 0
        freq = int(freq)
        self.send([12,freq])
        return bool(self.waitAck())

    def setOut1(self, state):
        if state == "OFF" or state == 0:
            self.send([14,0])
        elif state == "ON" or state == 1:
            self.send([14,1])
        return bool(self.waitAck())

    def setOut2(self, state):
        if state == "OFF" or state == 0:
            self.send([16,0])
        elif state == "ON" or state == 1:
            self.send([16,1])
        return bool(self.waitAck())

    def getAmpValue(self):
        self.send([20])
        response = self.waitAck()
        if response[2] == 148:
            value = (response[3]<<8) + (response[4])
            return value
        else:
            print("wrong response code")
            return None

    def getAnalog1(self):
        self.send([21])
        response = self.waitAck()
        if response[2] == 149:
            value = (response[3]<<8) + (response[4])
            return value
        else:
            print("wrong response code")
            return None
            
    def getAnalog2(self):
        self.send([22])
        response = self.waitAck()
        if response[2] == 150:
            value = (response[3]<<8) + (response[4]) 
            return value
        else:
            print("wrong response code")
            return None

    def getIn1(self):
        self.send([30])
        response = self.waitAck()
        if response[2] == 158:
            value = response[3]
            return value
        else:
            print("wrong response code")
            return None
    def getIn2(self):
        self.send([31])
        response = self.waitAck()
        if response[2] == 159:
            value = response[3]
            return value
        else:
            print("wrong response code")
            return None
    
    def setEncoderMode(self, mode):
        if mode == "QUADRATURE" or mode == 0:
            self.send([40,0])
        elif mode == "PWM" or mode == 1:
            self.send([40,1])
        return bool(self.waitAck())

    def setEncoderCount(self, count):
        if count < 0 or count > 2**32:
            print("Invalid count")
            return 0            
        self.send([42]+list(struct.unpack('4B', struct.pack('>I', count))))
        return bool(self.waitAck())
    
    def getEncoderCount(self):
        self.send([43])
        response = self.waitAck()
        if response[2] == 171:
            value = (response[3]<<24) + (response[4]<<16) + (response[5]<<8) + response[6]
            return value
        else:
            print("wrong response code")
            return None

    def getEncoderDuty(self):
        self.send([44])
        response = self.waitAck()
        if response[2] == 172:
            value = (response[3]<<8) + (response[4])
            return value
        else:
            print("wrong response code")
            return None

    def runAutoOffset(self):
        self.send([62]) 
        return bool(self.waitAck())

    def setGain(self, gain):
        if gain < 1:
            print("Invalid gain")
            return 0    
        self.send([54]+list(struct.unpack('2B', struct.pack('>h', gain))))
        return bool(self.waitAck())
        