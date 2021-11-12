import io
from picamera import PiCamera
import time
import os
from time import time, sleep
from datetime import datetime, timedelta

'''
post:https://forums.raspberrypi.com/viewtopic.php?t=106930
Not really software/hardware engineer but the timestamps work!
'''

class PtsOutput(object):
    def __init__(self, camera, video_filename, pts_filename):
        self.camera = camera
        self.video_output = io.open(video_filename, 'wb')
        self.pts_output = io.open(pts_filename, 'w')
        self.start_time = None
        self.frame_count = 0
        self.pts_output.write(f'StartTime: {time()}\n')
        self.pts_output.write('frame,Timestamp\n') # reference start timestamp

    def write(self, buf):
        self.video_output.write(buf)
        if self.camera.frame.complete and self.camera.frame.timestamp:
            self.pts_output.write(f'{self.frame_count},{self.camera.frame.timestamp}\n') # get stc timestamp, more accurate 
            self.frame_count +=1
    
    def flush(self):	
        self.video_output.flush()
        self.pts_output.flush()
        
    def close(self):
        self.video_output.close()
        self.pts_output.close()	

'''
slight addition to picamera library for path saves and timestamps
'''

class pts_picam():
    def __init__(self,camera_settings,pi_settings):
        self.pi_settings = pi_settings
        self.camera_settings = camera_settings
        data_path=pi_settings['data_path']
        tm = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.data_path = data_path + tm + '/'

    def setup(self):
        self.camera = PiCamera()
        self.camera.resolution = self.camera_settings['resolution']
        #self.camera.shutter_speed= self.camera_settings['shutter_speed']
        self.camera.framerate = self.camera_settings['framerate']
        #self.camera.awb_mode = self.camera_settings['awb_mode']
        self.camera.iso = self.camera_settings['iso']
        self.camera.sensor_mode = self.camera_settings['sensor_mode']
        #self.camera.awb_gains = self.camera_settings['awb_gains']
        #self.camera.exposure_mode = self.camera_settings['exposure_mode']
        self.camera.vflip = self.camera_settings['vertical_flip']
        self.camera.hflip = self.camera_settings['horizontal_flip'] 

    def record(self):
        pts_path= self.data_path+'timestamps.csv'
        file_path = self.data_path+'behavior.h264'
        print(file_path)
        self.camera.start_recording(PtsOutput(self.camera, file_path, pts_path), format='h264' ,level='4.2')
        if self.camera_settings['Display'] == 'True':
            self.camera.start_preview(fullscreen=False, \
                window=((10, 10, 256, 256)))

    def stop_record(self):
        if self.camera_settings['Display'] == 'True':
            self.camera.stop_preview()
        self.camera.stop_recording()

'''
#demo code
camera = PiCamera()
camera.resolution = (960,960)
#c
camera.framerate = 90
#camera.awb_mode = 'off'
#camera.awb_gains = (1,1)
file_path='/media/pi/Seagate Expansion Drive/New/test.h264'
pts_path='/media/pi/Seagate Expansion Drive/New/test.txt'
camera.start_recording(PtsOutput(camera, file_path, pts_path), format='h264' ,level='4.2')
camera.start_preview(fullscreen=False, window=((10, 10, 640, 480)))
while True:
    try:
        sleep(0.1)
    except KeyboardInterrupt:
        camera.stop_recording()
        break
'''