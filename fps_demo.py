from pi_video_stream_f import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2


vs=PiVideoStream('/home/pi/Documents')
vs.record(30)
