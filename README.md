# edf-accel-logger
Code for logging accelerometer data to an EDF file for medical diagnosis and analysis

Data from an MMA8451 tripl-axis accelerometer via a Teensy LC and regular USB serial is read from the USB serial port. The data is written to a file in EDF format. The reason for using EDF is it a good format for medical data exchange, and there are good viewers which facilitate reviewing data captures over a long time period.

Any micro could be used for the accelerometer, but the Teensy LC has the advantage of matching 3 of 4 pins of the Sparkfun MMA8451 breakout, which makes assembly very easy. The whole thing is small enough to tuck into a sock and be unobtrusive.

The Arduino code requires:
Adafruit_MMA8451
Adafruit_Sensor

The Adafruit MMA8451 library needs the following changes to use the second i2c bus on the Teensy LC so you can neatly connect them with a 3 pin header and a wire for GND:


`$ diff Adafruit_MMA8451_Library/Adafruit_MMA8451.cpp Adafruit_MMA8451_teensy_Library/Adafruit_MMA8451_teensy.cpp 
3c3
<     @file     Adafruit_MMA8451.h
---
>     @file     Adafruit_MMA8451_teensy.h
26,27c26,28
< #include <Wire.h>
< #include <Adafruit_MMA8451.h>
---
> #include <i2c_t3.h>
> #include <Adafruit_MMA8451_teensy.h>
> 
36c37
<   return Wire.read();
---
>   return Wire1.read();
38c39
<   return Wire.receive();
---
>   return Wire1.receive();
44c45
<   Wire.write((uint8_t)x);
---
>   Wire1.write((uint8_t)x);
46c47
<   Wire.send(x);
---
>   Wire1.send(x);
57c58
<   Wire.beginTransmission(_i2caddr);
---
>   Wire1.beginTransmission(_i2caddr);
60c61
<   Wire.endTransmission();
---
>   Wire1.endTransmission();
69c70
<     Wire.beginTransmission(_i2caddr);
---
>     Wire1.beginTransmission(_i2caddr);
71c72
<     Wire.endTransmission(false); // MMA8451 + friends uses repeated start!!
---
>     Wire1.endTransmission(false); // MMA8451 + friends uses repeated start!!
73,74c74,75
<     Wire.requestFrom(_i2caddr, 1);
<     if (! Wire.available()) return -1;
---
>     Wire1.requestFrom(_i2caddr, 1);
>     if (! Wire1.available()) return -1;
93c94,95
<   Wire.begin();
---
>   Wire1.begin(I2C_MASTER, 0x00, I2C_PINS_22_23, I2C_PULLUP_EXT, 400000);
>   Wire1.setDefaultTimeout(10000); // 10ms
102c104
<     return false;
---
>     //return false;
137c139
<   Wire.beginTransmission(_i2caddr);
---
>   Wire1.beginTransmission(_i2caddr);
139c141
<   Wire.endTransmission(false); // MMA8451 + friends uses repeated start!!
---
>   Wire1.endTransmission(false); // MMA8451 + friends uses repeated start!!
141,144c143,146
<   Wire.requestFrom(_i2caddr, 6);
<   x = Wire.read(); x <<= 8; x |= Wire.read(); x >>= 2;
<   y = Wire.read(); y <<= 8; y |= Wire.read(); y >>= 2;
<   z = Wire.read(); z <<= 8; z |= Wire.read(); z >>= 2;
---
>   Wire1.requestFrom(_i2caddr, 6);
>   x = Wire1.read(); x <<= 8; x |= Wire1.read(); x >>= 2;
>   y = Wire1.read(); y <<= 8; y |= Wire1.read(); y >>= 2;
>   z = Wire1.read(); z <<= 8; z |= Wire1.read(); z >>= 2;`

The python code requires:
pyedflib
