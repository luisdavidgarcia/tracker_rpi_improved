import sys
sys.path.append('..')
import os
from datetime import datetime

#import pi_video_stream


class datalogger():
    """Utility class that writes data to a txt file
    """
    def __init__(self, file_name, data_path):
        """Opens a txt file for writing and writes a banner
        
        :param file_name: name of file to write to, in this case the ID of the RFID reader
        :type file_name: string
        :param data_path: path to the folder in which log files are stored
        :type data_path: string
        """     
        if not os.path.exists(data_path):
                print("Creating data directory: ",data_path)
                os.makedirs(data_path)
        
        #Creating file
        logFileName = data_path + os.sep + "RFID_data_" + str(file_name) + ".csv" 
        self.logFile = open(logFileName, 'w', encoding="utf-8")
        self.logFile.write('Frame' + ',' + 'Time' + "\n")        

    def write_to_txt(self, frame_count):
        """Writes a row to the txt file. This function is for use of RFID reader datalogging.
        
        :param frame_count: global frame count when RFID pickup occurred
        :type frame_count: integer
        :param message: data read on RFID, i.e. the tag number
        :type message: integer
        """
        sttime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
        self.logFile.write(str(frame_count) + ',' + sttime + "\n")


    def setdown(self):
        """Saves and closes the text file
        """
        self.logFile.close()


'''
if __name__=="__main__":
    dl = datalogger('X', '/home/pi/rpi_utils')
    for i in range(200):
        dl.write_to_txt(i, time.time())
    dl.setdown()
'''
