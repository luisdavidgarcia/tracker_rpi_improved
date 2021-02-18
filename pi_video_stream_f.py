from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import time
from imutils.video import FPS
import time
from configparser import ConfigParser
from datetime import datetime
from frame_counter import *
from datalogger import datalogger
class PiVideoStream:
    def __init__(self,data_path):
        config = ConfigParser()
        config.read('config.ini')
        cfg = 'tracker_cage_record'
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = list(map(int, config.get(cfg, 'resolution').split(', ')))
        self.data_path=data_path
        self.camera.sensor_mode = int(config.get(cfg, 'sensor_mode'))
        #self.camera.framerate = int(config.get(cfg, 'framerate'))
        self.camera.iso = int(config.get(cfg, 'iso'))
        self.camera.shutter_speed=30000
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = (1,1)
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,format="bgr", use_video_port=True)
        self.datalogger = datalogger('all', self.data_path)
        #with open(self.data_path+'/frame_time.csv','w') as f:
        #        f.writelines('Frame' + ',' + 'Time' + "\n")
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.out = cv2.VideoWriter(self.data_path + '/raw.avi', cv2.VideoWriter_fourcc(*'DIVX'), self.camera.framerate, self.camera.resolution)
        self.frame = None
        self.stopped = False
    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self
    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            #start = time.time()
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
            #time.sleep(max(0.5 / (self.camera.framerate) - (time.time() - start), 0.0))
    def read(self):
        # return the frame most recently read
        return self.frame
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
    def record(self,duration):
        self.start()
        time.sleep(0.1)
        fps = FPS().start()
        frame_count=0
        if duration is None:
            while True:
                try:
                    # grab the frame from the threaded video stream and resize it
                    # to have a maximum width of 400 pixels
                    #start = time.time()
                    frame = self.read()
                    #frame = imutils.resize(frame, width=400)
                    # check to see if the frame should be displayed to our screen
                    self.out.write(frame)
                    self.datalogger.write_to_txt(frame_count)
                    frame_count+=1
                    fps.update()
                    #time.sleep(max(0.5 / (self.camera.framerate) - (time.time() - start), 0.0))
                except KeyboardInterrupt:
                    break
            fps.stop()
            print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
            print(str(frame_count))
            # do a bit of cleanup
            #cv2.destroyAllWindows()
            self.stop()
            self.out.release()
            self.datalogger.setdown()
            #get_video_frame_count(self.data_path)
        else:
            end_time = time.time()+ duration
            while time.time()<end_time:
                #start = time.time()
                frame = self.read()
                self.out.write(frame)
                self.datalogger.write_to_txt(frame_count)
                frame_count+=1
                fps.update()
                #time.sleep(max(0.5 / (self.camera.framerate) - (time.time() - start), 0.0))
            fps.stop()
            print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
            print(str(frame_count))
            # do a bit of cleanup
            #cv2.destroyAllWindows()
            self.stop()
            self.out.release()
            self.datalogger.setdown()
            #get_video_frame_count(self.data_path)
