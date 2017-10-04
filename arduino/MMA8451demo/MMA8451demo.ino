/**************************************************************************/
/*!
    @file     Adafruit_MMA8451.h
    @author   K. Townsend (Adafruit Industries)
    @license  BSD (see license.txt)

    This is an example for the Adafruit MMA8451 Accel breakout board
    ----> https://www.adafruit.com/products/2019

    Adafruit invests time and resources providing this open source code,
    please support Adafruit and open-source hardware by purchasing
    products from Adafruit!

    @section  HISTORY

    v1.0  - First release

    OKAY read below:
    I had to hack the MMA8451 library to handle the following:
    - make it work with I2C channel 2 (Wire1) on the Teensy LC, as this makes soldering much easier
    - take out the device ID verification, since I'm using a MMA8452 not an MMA8451
    
*/
/**************************************************************************/

//#include <Wire.h>
#include <Adafruit_MMA8451_teensy.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();

void setup(void) {  
  Serial.begin(115200);
  
  //Serial.println("Adafruit MMA8451 test!");

  if (! mma.begin()) {
    //Serial.println("Device not found, or something else is wrong.!");
    while (1);
  }
  //Serial.println("MMA8451 found!");
  
  mma.setRange(MMA8451_RANGE_2_G);
  
  //Serial.print("Range = "); Serial.print(2 << mma.getRange());  
  //Serial.println("G");
  
}

void loop() {
  // Read the 'raw' data in 14-bit counts
//  mma.read();
//  Serial.print(mma.x); Serial.print(",");
//  Serial.print(mma.y); Serial.print(",");
//  Serial.println(mma.z); 

//  /* Get a new sensor event */ 
  sensors_event_t event; 
  mma.getEvent(&event);

  /* Display the results (acceleration is measured in m/s^2) */
  // use x,y,z format
  Serial.print(event.acceleration.x); Serial.print(",");
  Serial.print(event.acceleration.y); Serial.print(",");
  Serial.println(event.acceleration.z);
  
//  /* Get the orientation of the sensor */
//  uint8_t o = mma.getOrientation();
  
//  switch (o) {
//    case MMA8451_PL_PUF: 
//      Serial.println("Portrait Up Front");
//      break;
//    case MMA8451_PL_PUB: 
//      Serial.println("Portrait Up Back");
//      break;    
//    case MMA8451_PL_PDF: 
//      Serial.println("Portrait Down Front");
//      break;
//    case MMA8451_PL_PDB: 
//      Serial.println("Portrait Down Back");
//      break;
//    case MMA8451_PL_LRF: 
//      Serial.println("Landscape Right Front");
//      break;
//    case MMA8451_PL_LRB: 
//      Serial.println("Landscape Right Back");
//      break;
//    case MMA8451_PL_LLF: 
//      Serial.println("Landscape Left Front");
//      break;
//    case MMA8451_PL_LLB: 
//      Serial.println("Landscape Left Back");
//      break;
//    }
//  Serial.println();
  // sample at about 100 Hz
  delay(10);
  
}
