# edf-accel-logger
Code for logging accelerometer data to an EDF file for medical diagnosis and analysis

Data from an MMA8451 tripl-axis accelerometer via a Teensy LC and regular USB serial is read from the USB serial port. The data is written to a file in EDF format. The reason for using EDF is it a good format for medical data exchange, and there are good viewers which facilitate reviewing data captures over a long time period.

Any micro could be used for the accelerometer, but the Teensy LC has the advantage of matching 3 of 4 pins of the Sparkfun MMA8451 breakout, which makes assembly very easy. The whole thing is small enough to tuck into a sock and be unobtrusive.

The Arduino code requires:
Adafruit_MMA8451
Adafruit_Sensor

Adafruit_MMA8451 needs some changes to work with the Teensy LC secondary i2c bus. The files are included here.

The python code requires:
pyedflib
