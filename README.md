# edf-accel-logger
Code for logging accelerometer data to an EDF file for medical diagnosis and analysis

Data from an MMA8451 tripl-axis accelerometer via a Teensy LC and regular USB serial is read from the USB serial port. The data is written to a file in EDF format. The reason for using EDF is it a good format for medical data exchange, and there are good viewers which facilitate reviewing data captures over a long time period.
