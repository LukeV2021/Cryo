from Lakeshore_Class import Lakeshore
from Keithley_Class import Keithley
import math
import time

global output
output = []

def execute(setpoint, ramprate, holdtime, current, samplerate, outputpath, outputname):
    #connects to the instruments
    lakeshore = Lakeshore(comport='COM1', baudrate = 1200)
    keithley = Keithley(current)

    keithley.connect()

    initialtemp = lakeshore.getTemp()

    # Sets units to Kelvin
    lakeshore.command('CUNI K')
    #print(my_instrument.query('CUNI?'))

    # Sets setpoint
    lakeshore.command('SETP ' + str(setpoint))
    # print(my_instrument.query('SETP?'))

    # Enables ramp rate and sets it value
    lakeshore.command('RAMPR ' + str(ramprate))
    # print(my_instrument.query('RAMPR?'))

    # Sets the autotuning status. 3 means PID
    lakeshore.command('TUNE 3')
    # print(my_instrument.query('TUNE?'))

    # Sets a curve for the sensor 09 is for Type K thermocouple
    lakeshore.command('ACUR 09')
    # print(my_instrument.query('ACUR?'))

    # 1 sets the ramp value to true and the lakeshore begins the ramp
    lakeshore.command('RAMP 1')

    deltaT = float(initialtemp) - float(setpoint)
    t = deltaT / float(ramprate) * 60
    n = math.ceil(t / float(samplerate))

    begindown = time.time()

    # Loops through all sample points collecting data while ramping down
    for i in range(n):
        # Gets temperature and sets it as current temp
        currenttemp = lakeshore.getTemp()
        currentres = keithley.GetSample()

        # Appends current temp to output data
        output.append([currenttemp, currentres])
        # Sleeps until next sample needs to be taken
        time.sleep(float(samplerate))     # Note: baud rate is very low

    enddown = time.time()

    print(enddown-begindown)

    beginhold = time.time()

    # Collects data during the hold time
    for i in range(math.ceil(float(holdtime) / float(samplerate) * 60)):
        currenttemp = lakeshore.getTemp()
        currentres = keithley.GetSample()
        output.append([currenttemp, currentres])
        time.sleep(float(samplerate))

    endhold = time.time()

    print(endhold-beginhold)

    # Sets the lakeshore setpoint back to room temp
    lakeshore.command('SETP ' + str(initialtemp))
    # variable for change in temp needed
    deltaT = initialtemp - float(setpoint)
    # variable for time it takes to ramp up
    t = deltaT / float(ramprate) * 60
    # variable for number of sample points during ramp up
    n = math.ceil(t / float(samplerate))

    beginup = time.time()
    # Collects data during the ramp up phase
    for i in range(n):
        currenttemp = lakeshore.getTemp()
        currentres = keithley.GetSample()
        output.append([currenttemp, currentres])
        time.sleep(float(samplerate))

    endup = time.time()
    print(endup-beginup)

    keithley.Abort()

    print(output)

    generateReport(output, outputpath, outputname)

    return output

def DisplayTemp():
    if output == []:
        return 0
    else:
        return float(output[-1][0])

def generateReport(output, outputpath, outputname):
    # if the output path is not blank, write a text file to the specified destination
    if outputpath != '':
        outputfile = open(outputpath + "\\" + outputname + ".txt", "w")
    # if the output path is blank, write a text file in the same folder as the program
    else:
        outputfile = open(outputname + ".txt", "w")
    # Loops through the output data and generates a report with the following columns: temperature then resistance
    for i in range(len(output)):
        outputfile.write(str(output[i][0]) + "\t" + str(output[i][1]) + "\n")
    outputfile.close()

if __name__ == "__main__":
    setpoint = str(250)
    ramprate = str(80)
    holdtime = str(0.166)
    current = str(0.000001)
    samplerate = str(5)
    run(setpoint, ramprate, holdtime, current, samplerate)
    print(output)