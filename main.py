import time
import schedule
from datetime import datetime, timedelta
import datetime as dt
import os
import sys
import signal
#from udp_socket import rpi_socket
import RPi.GPIO as GPIO
sys.path.append('..')
from pi_video_stream_f import PiVideoStream
from RFID_reader import RFID_reader
#from tunnel_reader import tunnel_RFID_reader
from configparser import ConfigParser
from threading import Thread
import frame_counter as fc
from datalogger import datalogger


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
        self.port=int(config.get(cfg,'port'))
        self.ip=config.get(cfg,'ip')
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
        with open(self.data_path+'/text.csv',"a") as RFIDs:
                RFIDs.write('Reader,Timestamp,RFID\n')
        #self.reader0 = tunnel_RFID_reader('/dev/ttyUSB5',self.data_path+'/text.csv',17)
        self.reader0 = RFID_reader('/dev/ttyUSB0', '0',self.data_path+'/text.csv')
        self.reader1 = RFID_reader('/dev/ttyUSB1', '1',self.data_path+'/text.csv')
        self.reader2 = RFID_reader('/dev/ttyUSB2', '2',self.data_path+'/text.csv')
        self.reader3 = RFID_reader('/dev/ttyUSB3', '3',self.data_path+'/text.csv')
        self.reader4 = RFID_reader('/dev/ttyUSB4', '4',self.data_path+'/text.csv')
        self.reader5 = RFID_reader('/dev/ttyUSB5', '5',self.data_path+'/text.csv')
        #self.reader6 = RFID_reader('/dev/ttyUSB6', '6')
        #self.spt_socket=rpi_socket(self.ip, self.port,self.data_path+'/text.csv')
    def run(self):
        """Main function that opens threads and runs :class: 'pi_video_stream' in main thread. In each thread,
         :class:'RFID_reader' checks for RFID pickup. The pickup data is then logged to a text file 
         by :class: 'pi_video_stream'.
        """
        # Make threads for different objects
        t_rfid0 = Thread(target=self.reader0.scan, daemon=True)
        t_rfid1 = Thread(target=self.reader1.scan, daemon=True)
        t_rfid2 = Thread(target=self.reader2.scan, daemon=True)
        t_rfid3 = Thread(target=self.reader3.scan, daemon=True)
        t_rfid4 = Thread(target=self.reader4.scan, daemon=True)
        t_rfid5 = Thread(target=self.reader5.scan, daemon=True)
        #t_rfid6 = Thread(target=self.reader6.scan, daemon=True)
        #s_rfid=Thread(target=self.spt_socket.run, daemon=True)
        # Start threads
        t_rfid0.start()
        t_rfid1.start()
        t_rfid2.start()
        t_rfid3.start()
        t_rfid4.start()
        t_rfid5.start()
        #s_rfid.start()
        #t_rfid6.start()2q
        # keyboard interrupt handler, stops program once ctrl-c is pressed
        def keyboardInterruptHandler(signal, frame):
            self.setdown()
            exit(0)
        signal.signal(signal.SIGINT, keyboardInterruptHandler)

        # Start recording
        self.video.record(self.record_time_sec)
        

    def setdown(self):
        """Shuts down the :class:'pi_video_stream' object and :class:'RFID_reader' objects. 
        Note that this method has to execute for the video and txt files to save properly.
        """

        

        # Displays the fps and frame counts on terminal
        #fc.get_video_frame_count(rc.data_path)
        #fc.get_txt_frame_count(rc.data_path)

        # Post process the video to match FPS if specified by user

#def main_func():
#     rc = rpi_recorder()
#     rc.run()
#     time.sleep(30)
#     try: 
#        schedule.cancel(main_func)
#     except Exception as e:
#        print(e)
#        schedule.every(30).seconds.do(main_func)



if __name__ == "__main__":
     rc = rpi_recorder()
     rc.run()
     print("Finished recording at "+str(datetime.now()))
  
