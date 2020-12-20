from smbus import SMBus
import os
import sys
import time
import signal
from datetime import datetime
import RPi.GPIO as GPIO
from RFIDTagReader import RFIDTagReader
from RFIDTagReader.RFIDTagReader import TagReader
import pi_video_stream
from datalogger import datalogger
class tunnel_RFID_reader():
    def __init__(self, pin,pathin,tag_in_range_pin):
        """Constructor for a USB RFID reader-based RFID module.
        
        :param pin: RFID port number, usually a USB port
        :type pin: string
        :param ID: label to the RFID
        :type ID: string
        :param data_path: path to store the RFID reading information, defaults to None
        :type data_path: string
        """
        global globalReader
        global globalTag
        #GPIO.setmode(GPIO.BOARD)
        self.tag_in_range_pin= tag_in_range_pin
        self.reader = TagReader (pin, doChecksum = True, timeOutSecs = None, kind='ID')
        self.reader.installCallback(self.tag_in_range_pin)
        self.data = 0
        self.ID = 'tunnel'
        self.pathin=pathin


    def scan(self):
        while True:
           if RFIDTagReader.globalTag ==0:
               time.sleep(0.01)
           else:
               self.data= RFIDTagReader.globalTag
               with open(self.pathin,"a") as RFIDs:
                   RFIDs.write(str(self.ID)+'_in'+','+str(datetime.now())+','+str(self.data)+'\n')
               print(f"tag {str(self.data)} entered tunnel at {str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f'))}")
               while RFIDTagReader.globalTag==self.data:
                   while GPIO.input(self.tag_in_range_pin)==GPIO.HIGH:
                       pass
                   else: 
                       with open(self.pathin,"a") as RFIDs:
                           RFIDs.write(str(self.ID)+'_out'+','+str(datetime.now())+','+str(self.data)+'\n')
                       print(f"tag {str(self.data)} left tunnel at {str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f'))}")
                       RFIDTagReader.globalTag=0
                          
