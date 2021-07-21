"""Implements functionality unique to the Lake Shore Model 321 cryogenic temperature controller"""
import serial
import lakeshore
import time
import struct
from lakeshore.generic_instrument import GenericInstrument

class Lakeshore():
    """A class object representing the Lake Shore Model 321 cryogenic temperature controller"""

    def __init__(self, comport, baudrate):
        self.baud_rate= baudrate
        self.serial_number=None
        self.com_port=comport
        self.data_bits=7
        self.stop_bits=1
        self.parity=serial.PARITY_ODD
        self.flow_control=False
        self.handshaking=False
        self.timeout=2.0
        self.ser = serial.Serial(self.com_port, self.baud_rate, self.data_bits, self.parity, self.stop_bits, self.timeout)

    def query(self, string):
        query = str.encode(string)
        self.ser.write(query)
        data = self.ser.read_until()
        return data

    def command(self, string):
        command = str.encode(string)
        time.sleep(0.8)
        self.ser.write(command)
        time.sleep(0.8)

    def getTemp(self):
        data = self.query('CDAT?')
        temp = str(data.split())
        output = float(temp[4:len(temp)-2])
        return output

    def getID(self):
        data = self.query('*IDN?')
        name = str(data.split())
        ID = name[3:len(name)-2]
        self.serial_number = ID
        time.sleep(0.8)
        return ID

if __name__ == "__main__":
    my_instrument = Lakeshore(comport='COM1', baudrate = 1200)
    print("Connected to: " + my_instrument.getID())
    temp = my_instrument.getTemp()
    print(temp)

