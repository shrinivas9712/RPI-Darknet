from picamera import PiCamera
from subprocess import Popen, PIPE
import threading
from time import sleep
import os, fcntl
import time


camera = PiCamera()
camera.resolution = (512, 512)
camera.exposure_mode = 'sports'
camera.vflip = True

camera.capture('/tmp/in.jpg')
sleep(0.1)

# yolo_proc = Popen(["./darknet",
#                    "detector", "test", "./cfg/coco.data",
#                    "./cfg/yolov3-tiny.cfg",
#                    "./yolov3-tiny.weights",
#                    "-thresh","0.1",
#                    "-out", "/tmp/out"],
#                    stdin = PIPE, stdout = PIPE)

yolo_proc = Popen(["./darknet",
                   "detector", "test", "./cfg/tennis.data",
                   "./cfg/yolov3-tennis.cfg",
                   "./3_mix.weights",
                   "-thresh","0.1",
                   "-out", "/tmp/out"],
                   stdin = PIPE, stdout = PIPE)

fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

while True:
    try:
        stdout = yolo_proc.stdout.read()
        if stdout is not None:
            print "STDout", stdout
        # if stdout is None:
        #     continue
        if 'BBOX' in stdout:
            print stdout
        if 'Enter Image Path' in stdout:
            camera.capture('/tmp/in.jpg')
            yolo_proc.stdin.write('/tmp/in.jpg\n')
    except Exception:
        pass
