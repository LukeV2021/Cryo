# Imports libraries needed
import serial
import numpy as np
import time
import lakeshore
from lakeshore.generic_instrument import GenericInstrument
import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi
from CompiledGUI import Ui_LakeshoreGUI
from Lakeshore_Class import Lakeshore
from Keithley_Class import Keithley
from GUI_Class import Window

# Function that connects 321 and sets up a class.
def connect():
    try:
        # From the Model321_Setup.py, initializes my instrument
        lakeshore = Lakeshore(comport='COM1', baudrate = 1200)
        # From the Model321_Setup.py, identifies the ID number
        ID = lakeshore.getID()
        # Trims the ID to just be the useful characters
        if len(ID) < 4:
            # If no Lakeshore is found, raise an error.
            raise Exception('Lakeshore device not found. Ensure device is plugged in and powered.')
        else:
            # If Lakeshore is found, print ID
            print("Connected to Lakeshore: " + ID)
    except:
        raise Exception('Lakeshore device not found. Ensure device is plugged in and powered.')

    try:
        keithley = Keithley(0.000001)
        IDN = str(keithley.getID())
        print("Connected to Keithley: " + IDN)
    except:
        raise Exception('Keithley device not found. Ensure device is plugged in and powered.')

# Function that uses generic code to open and run the GUI
def run():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

connect()
run()