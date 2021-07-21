# To convert .ui files to .py files, enter line below in terminal
# python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py

# Useful imports
import sys
import time
import math
import threading
import concurrent.futures

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from CompiledGUI import Ui_LakeshoreGUI
from Lakeshore_Class import Lakeshore
from RampDown_Hold_RampUp import execute, DisplayTemp


# Main window class
class Window(QMainWindow, Ui_LakeshoreGUI):
    def __init__(self, parent=None):
        # Generic variables for GUI
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        # inputs for the GUI
        self.targettemp = None
        self.ramprate = None
        self.holdtime = None
        self.deltamodecurrent = None
        self.measurementrate = None
        self.outputname = None
        self.outputpath = None
        self.currenttemp = None
        self.currenttemp2 = None
        self.programname = None
        self.programpath = None
        self.output = []

    # Function that handles events
    def connectSignalsSlots(self):
        # if the exit button is clicked the close function runs
        self.Exit.clicked.connect(self.close)
        # if thclosee about button is clicked the about function runs
        self.About.clicked.connect(self.about)
        # If the apply changes button is clicked the getinfo function runs
        self.ApplyChanges.clicked.connect(self.getinfo)

    def about(self):
        # Brings up a message box when the about button is clicked.
        QMessageBox.about(
            self,
            "About Lakeshore & Keithley User Interface",
            "<p>Interface for Model 321 Lakeshore Temperature Controller made with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>"
            "<p>- Luke Vaughan</p>",
        )

    # Function that reads the users inputs from the GUI and stores them in a class variable.
    # Once user input is read, the run() function is called.
    def getinfo(self):
        #reads user input
        self.targettemp = float(self.TempSetpoint.text())
        self.ramprate = float(self.RampRate.text())
        self.holdtime = float(self.HoldTime.text())
        self.deltamodecurrent = float(self.DeltaModeCurrent.text())
        self.measurementrate = float(self.MeasurementRate.text())
        self.outputname = str(self.OutputName.text())
        self.outputpath = str(self.OutputPath.text())
        self.run()

    # Function that sends commands to the Lakeshore
    def run(self):
        #execute(self.targettemp, self.ramprate, self.holdtime, self.deltamodecurrent, self.measurementrate)
        x = threading.Thread(target=execute, args=(self.targettemp, self.ramprate, self.holdtime, self.deltamodecurrent, self.measurementrate, self.outputpath, self.outputname))
        y = threading.Thread(target=self.UpdateTemp)
        #z = threading.Thread(target=self.CheckThreads(x))

        x.start()
        y.start()

        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(execute, self.targettemp, self.ramprate, self.holdtime, self.deltamodecurrent, self.measurementrate)
            return_value = future.result()
            print(return_value)
        """

    def UpdateTemp(self):
        while True:
            if threading.active_count() == 3:
                temp = DisplayTemp()
                self.CurrentTemp.display(temp)
                time.sleep(0.5)
            else:
                break

    """
    def CheckThreads(self, x):
        while x.is_alive() == True:
            continue
        self.generateReport(self.output)
    """


    # Function that generates a report from the collected output data
    def generateReport(self, output):
        # if the output path is not blank, write a text file to the specified destination
        if self.outputpath != '':
            outputfile = open(self.outputpath + "\\" + self.outputname + ".txt", "w")
        # if the output path is blank, write a text file in the same folder as the program
        else:
            outputfile = open(self.outputname + ".txt", "w")
        # Loops through the output data and generates a report with the following columns: temperature then resistance
        for i in range(len(output)):
            outputfile.write(str(output[i][0]) + "\t" + str(output[i][1]) + "\n")
        outputfile.close()

# Generic code for running the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())