# restless leg and periodic limb movement monitor
# uses a 3-axis accellerometer through a Teensy LC USB serial
# saves files in EDF format for use in edfbrowser

from __future__ import division, print_function, absolute_import

import sys, getopt
import serial
import time
import pyedflib
import numpy as np
import Queue
import threading

def usage():
    print("accellog.py ouputfile")

class mySerial(threading.Thread):
    def __init__(self, queue):
        port = "/dev/ttyACM0"
        baud = 115200

        super(mySerial, self).__init__()
        self.queue = queue
        self.buffer = ''
        self.ser = serial.Serial(port, baud, timeout=10)

    def run(self):
        while True:
            self.buffer += self.ser.read(self.ser.inWaiting())
            if '\n' in self.buffer:
                var, self.buffer = self.buffer.split('\n', 1)
                self.queue.put(var)

class Base():
    def __init__(self):
        self.queue = Queue.Queue(0)
        self.ser = mySerial(self.queue)
        self.ser.daemon = True
        self.ser.start()
 

    def main(self, *args):
        outfile = ''
        try:
            opts, args = getopt.getopt(sys.argv[1:],"ho:",["help","ofile="])
        except getopt.GetoptError as err:
            print(err)
            usage()
            sys.exit(2)
    
        if not opts:
            usage()
            sys.exit(1)
    
        for opt, arg in opts:
            if opt == '-h':
                usage()
                sys.exit()
            elif opt in ("-o", "--ofile"):
                outfile = arg
        channel_info = []
     
     
        try:
            #f = open(outfile,'w')
            # create an EDF file handle with three channels
            f = pyedflib.EdfWriter(outfile, 3, file_type=pyedflib.FILETYPE_EDFPLUS)
        except IOError:
            print("Unable to open file %s" % (outfile))
            print("Exiting.")
            sys.exit(1)
    
    
        ch_dict = {'label': 'accel_x', 'dimension': 'm/s^2', 'sample_rate': 100, 'physical_max': 19.6, 'physical_min': -19.6, 'digital_max': 8191, 'digital_min': -8191, 'transducer': '', 'prefilter':''}
        channel_info.append(ch_dict)
    
        ch_dict = {'label': 'accel_y', 'dimension': 'm/s^2', 'sample_rate': 100, 'physical_max': 19.6, 'physical_min': -19.6, 'digital_max': 8191, 'digital_min': -8191, 'transducer': '', 'prefilter':''}
        channel_info.append(ch_dict)
    
        ch_dict = {'label': 'accel_z', 'dimension': 'm/s^2', 'sample_rate': 100, 'physical_max': 19.6, 'physical_min': -19.6, 'digital_max': 8191, 'digital_min': -8191, 'transducer': '', 'prefilter':''}
        channel_info.append(ch_dict)
    
    
        f.setSignalHeaders(channel_info)


        while(True):
            try:
                # numpy array to hold all the data
                myList = np.zeros(300)
                # numpy arrays to hold each channel's data
                myX = np.zeros(100)
                myY = np.zeros(100)
                myZ = np.zeros(100)
                x = 0
            except KeyboardInterrupt:
                print("Exiting.")
                f.blockWritePhysicalSamples(myList)
                f.close()
                sys.exit()

            while x < 100:
                try:
                    var = self.queue.get(False)
                except Queue.Empty:
                    pass
                except KeyboardInterrupt:
                    print("Exiting.")
                    # write out the samples even if incomplete
                    # otherwise the edf reader complains the data doesn't
                    # match the header
                    f.blockWritePhysicalSamples(myList)
                    f.close()
                    sys.exit()
                else:
                    myPacket = np.fromstring(var, dtype=float, sep=",")
                    # data is sent az "x,y,z"
                    # load into arrays per channel
                    myX[x] = myPacket[0]
                    myY[x] = myPacket[1]
                    myZ[x] = myPacket[2]
                    x += 1
            try:
                # stupidly copy the channels back in serial format
                # there must be a better way to do this
                x = 0
                for p in range(0, 99):
                    myList[x] = myX[p]
                    x += 1
                for p in range(0, 99):
                    myList[x] = myY[p]
                    x += 1
                for p in range(0, 99):
                    myList[x] = myZ[p]
                    x += 1 
                # write the channels to the edf file
                f.blockWritePhysicalSamples(myList)
                # show we are running
                print('.') 
            except IOError:
                print("Unable to write to file %s" % (outfile))
                break
            except KeyboardInterrupt:
                print("Exiting.")
                f.blockWritePhysicalSamples(myList)
                f.close()
                sys.exit()

if __name__ == '__main__':
    b = Base()
    b.main()

