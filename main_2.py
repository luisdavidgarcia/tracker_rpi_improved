from time import time, sleep
from datetime import datetime, timedelta
from udp_socket import rpi_socket
from RFID_reader import RFID_reader
from settings_loader import camera_settings, pi_settings
from pts_picamera import pts_picam
from threading import Thread, current_thread
import multiprocessing
import os



class rpi_recorder():
    """:class: 'rpi_recorder' is the top level class of natural mouse tracker. It creates :class: 'RFID_reader' objects
    which run in separate threads, and also runs camera recording in the main loop. User config files can be found in 
    'config.ini'
    """

    def __init__(self):
        """Constructor for :class: 'recorder'. Loads the config file 'config.ini' and creates a :class:'pi_video_stream' 
        object and four :class:'RFID_reader' objects.
        """
        # Load settings
        self.pi_settings = pi_settings('config.ini')
        self.camera_settings = camera_settings('config.ini')
    
    def setup(self):
        tm = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
        self.data_path = self.pi_settings['data_path'] + '/'+ tm
        os.mkdir(self.data_path) 
        #setup camera
        self.camera = pts_picam(self.camera_settings,self.pi_settings)
        self.camera.setup()
        # Making directory
      
        # thread setup for RFID reading

        if self.pi_settings['spt']:
            self.spt_socket=rpi_socket(self.pi_settings['ip'], self.pi_settings['port'],self.data_path+'/spt_text.csv')

    def run(self):
        """Main function that opens threads and runs :class: 'pi_video_stream' in main thread. In each thread,
         :class:'RFID_reader' checks for RFID pickup. The pickup data is then logged to a text file 
         by :class: 'pi_video_stream'.
        """
        # start threads and multiprocess
        if self.pi_settings['rfid']:
            #readers=["self.reader{}=RFID_reader('/dev/ttyUSB{}', '{}',self.data_path+'/text{}.csv')".format(i,i,i,i) for i in range(self.nreaders)]
            readers=["self.reader{}=RFID_reader('/dev/ttyUSB{}', '{}',self.data_path+'/RFID_reads.csv')".format(i,i,i)\
                 for i in range(self.pi_settings['nreaders'])]
            for i in readers:
                exec(i)
        if self.pi_settings['rfid']:
            #reader_process=["t_rfid{}=multiprocessing.Process(target=self.reader{}.scan,daemon=True)".format(i,i) for i in range(self.nreaders)]
            reader_process=["t_rfid{}=Thread(target=self.reader{}.scan,daemon=True)".format(i,i) \
                for i in range(self.pi_settings['nreaders'])]
            for i in reader_process:
                exec(i) 
        if self.pi_settings['rfid']=='True':
            s_rfid=multiprocessing.Process(target=self.spt_socket.run, daemon=True)
        # Start Processes
        if self.pi_settings['rfid']:
            reader_startup=["t_rfid{}.start()".format(i) for i in range(self.pi_settings['nreaders'])]
            for i in reader_startup:
                exec(i)
        if self.pi_settings['spt']:
            s_rfid.start()
        self.camera.record()
        if self.pi_settings['user_interrupt_only']:
            start_time = time()
            while True:
                try:
                    sleep(0.0000001)
                except KeyboardInterrupt:
                    self.camera.stop_recording()
        else:
            start_time = time()
            end_time = start_time + self.pi_settings['duration']
            current_time = time()
            while current_time <= end_time:
                try:
                    current_time = time()
                except KeyboardInterrupt:
                    break
            self.camera.camera.stop_recording()
        dur = time() - start_time  
        print(f' Recorded for {dur} seconds ')
        print(f' total of  {self.camera.camera.frame_count} frames recorded')
        print("Finished recording at "+str(datetime.now()))


if __name__ == "__main__":
     rc = rpi_recorder()
     rc.setup()
     rc.run()
     print("Finished recording at "+str(datetime.now()))
