from picamera import PiCamera
from subprocess import Popen, PIPE
from time import sleep
import os, fcntl
import time

from UDPComms import Publisher

pub = Publisher(8390)

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
            print "STDOUT", stdout

        if 'Enter Image Path' in stdout:
            camera.capture('/tmp/in.jpg')
            yolo_proc.stdin.write('/tmp/in.jpg\n')

            msg = []
            if 'BBOX' in stdout:
                lines = stdout.split('\n')
                markers = (line for line in lines if 'BBOX' in line)
                for mark in markers:
                    _,x,y,w,h,prob = mark.split(' ')
                    msg.append({'x':x,
                        'y':y,
                        'w':w,
                        'h':h,
                        'prob':prob})
            pub.send(msg)

    except IOError:
        pass
