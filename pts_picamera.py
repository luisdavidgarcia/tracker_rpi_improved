import io
from picamera import PiCamera
import time
from time import time, sleep


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
        self.pts_output.write('# frame, tdiff, timestamp\n')

    def write(self, buf):
        self.video_output.write(buf)
        if self.camera.frame.complete and self.camera.frame.timestamp:
            if self.start_time is None:
                self.start_time = self.camera.frame.timestamp
            self.pts_output.write('%f\n' % ((self.camera.frame.timestamp - self.start_time) / 1000.0))
            self.pts_output.write('%f\n' % ((self.camera.frame.timestamp - self.start_time) / 1000.0))
            self.pts_output.write(f'{self.frame_count},{((self.camera.frame.timestamp - self.start_time) / 1000.0)},{time()}\n')
            #self.pts_output.write(f'{self.frame_count},{self.camera.frame.timestamp}\n')
            self.frame_count +=1
    
    def flush(self):	
        self.video_output.flush()
        self.pts_output.flush()
        
    def close(self):
        self.video_output.close()
        self.pts_output.close()	

'''
class to setup picamera and save timestamps of frames
'''

class pts_picam():
    def __init__(self,camera_settings):
        self.settings = camera_settings
        data_path=pi_settings['data_path']
        self.data_path = data_path + tm + '/'

    def setup(self):
        self.camera = PiCamera()
        self.camera.resolution = self.settings['resolution']
        self.camera.shutter_speed= self.settings['shutter_speed']
        self.camera.framerate = self.settings['framerate']
        self.camera.awb_mode = self.settings['awb_mode']
        self.camera.iso = self.settings['iso']
        self.camera.sensor_mode = self.settings['sensor_mode']
        self.camera.awb_gains = self.settings['awb_gains']
        self.camera.exposure_mode = self.settings['exposure_mode']
        self.camera.vflip = self.settings['vertical_flip']
        self.camera.hflip = self.settings['horizontal_flip'] 

    def record(self):
        pts_path= self.data_path+'pts.csv'
        file_path = self.data_path+'raw.h264'
        self.camera.start_recording(PtsOutput(self.camera, file_path, pts_path), format='h264' ,level='4.2')
        if self.settings['Display'] == 'True':
            self.camera.start_preview(fullscreen=False, \
                window=((10, 10,self.settings['resolution'][0] , self.settings['resolution'][0])))



'''
#demo code
camera = PiCamera()
camera.resolution = (640,480)
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
