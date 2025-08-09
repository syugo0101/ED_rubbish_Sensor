import numpy as np
import cv2

class CountArea:
    def __init__(self, lower_hsv, upper_hsv):
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv

    def get_white_area(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        area = cv2.countNonZero(mask)
        return area, mask