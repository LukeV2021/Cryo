import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import time

# setup for resource manager and naming the instrument
class Keithley():
    def __init__(self, current):
        self.keithley = None
        self.current = current * 10 ** -6
        self.values = None

    def connect(self):
        rm = pyvisa.ResourceManager()
        self.keithley = rm.open_resource("GPIB::1::INSTR")
        #IDN = self.keithley.write("*IDN?")
        #print(IDN)
        self.keithley.write("SOUR:DELT:HIGH " + str(self.current))
        # Arms the 6220 in delta mode
        self.keithley.write("DELTa:ARM")
        self.keithley.write("UNIT OHMS")
        #begin sweep
        self.keithley.write("INIT:IMM")
        time.sleep(3)

    def getID(self):
        rm = pyvisa.ResourceManager()
        self.keithley = rm.open_resource("GPIB::1::INSTR")
        IDN = self.keithley.write("*IDN?")
        return IDN

    def GetSample(self):
        self.values = []
        samples = 10
        for n in range(1, samples):
            self.values.append(self.keithley.query_ascii_values('SENS:DATA:FRESh?'))

        #print(self.values)
        #print(len(self.values))

        #self.keithley.write("*RST")

        sum = 0
        for i in range(len(self.values)):
            sum = sum + self.values[i][0]

        average = sum / len(self.values)

        #print(str(round(average)) + " OHMS")
        return average

    def PlotResults(self):
        x = [x for x, y in self.values]
        y = [y for x, y in self.values]
        plt.ylabel('Resistance (Ohms)')
        plt.xlabel('Time (ms)')
        plt.plot(y,x)
        plt.show()

    def Abort(self):
        self.keithley.write("SOUR:SWE:ABOR")

if __name__ == "__main__":
    my_instrument = Keithley(2)
    print(my_instrument.getID())
    my_instrument.connect()
    print(my_instrument.GetSample())
    time.sleep(5)
    print(my_instrument.GetSample())
    my_instrument.Abort()
