import time
import schedule
from datetime import datetime, timedelta
import datetime as dt
import os
import sys
import signal
from udp_socket import rpi_socket
from pi_video_stream_f import PiVideoStream
from RFID_reader import RFID_reader
from configparser import ConfigParser
from threading import Thread
import frame_counter as fc
from datalogger import datalogger
import multiprocessing



class rpi_recorder():
    """:class: 'rpi_recorder' is the top level class of natural mouse tracker. It creates :class: 'RFID_reader' objects
    which run in separate threads, and also runs camera recording in the main loop. User config files can be found in 
    'config.ini'
    """

    def __init__(self):
        """Constructor for :class: 'recorder'. Loads the config file 'config.ini' and creates a :class:'pi_video_stream' 
        object and four :class:'RFID_reader' objects.
        """
        # Load configs
        config = ConfigParser()
        config.read('config.ini')
        cfg = 'tracker_cage_record'
        # Making directory
        self.data_root = config.get(cfg, 'data_root')
        self.spt=config.get(cfg,'spt')
        self.port=int(config.get(cfg,'port'))
        self.ip=config.get(cfg,'ip')
        self.nreaders=int(config.get(cfg,'nreaders'))
        self.rfid=config.get(cfg,'rfid')
        tm = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.data_path = self.data_root + tm
        # Object and settings for recording
        self.video = PiVideoStream(self.data_path)
        self.user_interrupt_only = config.get(cfg, 'user_interrupt_only')
        if self.user_interrupt_only == "True":
            self.record_time_sec = None        
        else:
            self.record_time_sec = int(config.get(cfg, 'record_time_sec'))
        # Object for RFID reading
        if self.rfid =='True':
            readers=["self.reader{}=RFID_reader('/dev/ttyUSB{}', '{}',self.data_path+'/text{}.csv')".format(i,i,i,i) for i in range(self.nreaders)]
            for i in readers:
                exec(i)
        if self.spt== 'True':
            self.spt_socket=rpi_socket(self.ip, self.port,self.data_path+'/spt_text.csv')
    def run(self):
        """Main function that opens threads and runs :class: 'pi_video_stream' in main thread. In each thread,
         :class:'RFID_reader' checks for RFID pickup. The pickup data is then logged to a text file 
         by :class: 'pi_video_stream'.
        """
        # Make threads for different objects
        if self.rfid =='True':
            reader_process=["t_rfid{}=multiprocessing.Process(target=self.reader{}.scan,daemon=True)".format(i,i) for i in range(self.nreaders)]
            for i in reader_process:
                exec(i)
        if self.spt=='True':
            s_rfid=multiprocessing.Process(target=self.spt_socket.run, daemon=True)
        # Start Processes
        if self.rfid =='True':
            reader_startup=["t_rfid{}.start()".format(i) for i in range(self.nreaders)]
            for i in reader_startup:
                exec(i)
        if self.spt=='True':
            s_rfid.start()
        self.video.record(self.record_time_sec)
if __name__ == "__main__":
     rc = rpi_recorder()
     rc.run()
     print("Finished recording at "+str(datetime.now()))
