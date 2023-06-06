import os.path as osp 

from pyparrot.Bebop import Bebop
from pyparrot.DroneVision import DroneVision
import threading
import cv2
import time
import run_person_detector as detector
import numpy as np

def move(bebop : Bebop, barycenter):
    bx = barycenter[0]
    by = barycenter[1]

    if (bx > 260):
        bebop.move_relative(.1,0,0,0)
    elif (bx < 240):
        bebop.move_relative(-.1,0,0,0)

