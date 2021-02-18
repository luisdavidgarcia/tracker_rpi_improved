from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import time
from imutils.video import FPS
import time
from frame_counter import *
class PiVideoStream:
    def __init__(self, data_path,resolution=(512, 400), framerate=90):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.sensor_mode = 6
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,format="bgr", use_video_port=True)
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.data_path=data_path
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
    def read(self):
        # return the frame most recently read
        return self.frame
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
    def record(self,Display=True):
        self.start()
        time.sleep(1.0)
        fps = FPS().start()
        frame_count=0
        while True:
            try:
                # grab the frame from the threaded video stream and resize it
                # to have a maximum width of 400 pixels
                frame = self.read()
                #frame = imutils.resize(frame, width=400)
                # check to see if the frame should be displayed to our screen
                self.out.write(frame)
                #if Display:
                #    cv2.imshow("Frame", frame)
                #    key = cv2.waitKey(1) & 0xFF
                    #update the FPS counter
                frame_count+=1
                fps.update()
            except KeyboardInterrupt:
                break
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        print(str(frame_count))
        # do a bit of cleanup
        cv2.destroyAllWindows()
        self.stop()
        get_video_frame_count(self.data_path)

