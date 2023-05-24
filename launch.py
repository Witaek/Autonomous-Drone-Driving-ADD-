from pyparrot.Bebop import Bebop
from pyparrot.DroneVision import DroneVision
import threading
import cv2
import time
import run_person_detector as detector
import numpy as np


isAlive = False

class UserVision:
    def __init__(self, vision, bebop):
        self.index = 0
        self.vision = vision
        self.last_picture_time = time.time()
        self.drone = bebop

    def save_pictures(self, args):
        current_time = time.time()
        time_diff = current_time - self.last_picture_time
        if time_diff < 1:
            # wait until one second has passed since last picture
            return
        self.last_picture_time = current_time

        img = self.vision.get_latest_valid_picture()
        if img is not None:
            #filename = "test_image_%06d.png" % self.index
            result, coordinates = detector.run_object_detection(img)
            #cv2.imwrite(filename, img)
            self.index += 1

            print(coordinates)

            # Read the saved image and display it
            #image = cv2.imread(filename)
            cv2.imshow("Image", result.astype(np.uint8))
            cv2.waitKey(1)  # Add a small delay to allow GUI to refresh

# make my bebop object
bebop = Bebop()

# connect to the bebop
success = bebop.connect(5)
bebop.set_max_altitude(2)
if success:
    # start up the video
    bebopVision = DroneVision(bebop, is_bebop=True)

    userVision = UserVision(bebopVision, bebop)
    bebopVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
    success = bebopVision.open_video()
    bebop.safe_takeoff(10)
    bebop.smart_sleep(2)
    bebop.move_relative(0,0,-1,0)

    if success:
        print("Vision successfully started!")

        bebop.smart_sleep(15)
        bebop.safe_land(10)
        bebopVision.close_video()

    # disconnect nicely so we don't need a reboot
    bebop.disconnect()
else:
    print("Error connecting to bebop. Retry")
