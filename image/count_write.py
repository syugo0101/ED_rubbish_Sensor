
import cv2
import numpy as np

# 画像を読み込み指定色領域のピクセル数カウント
class CountWhiteArea:
    def __init__(self, path,white_ranges):
        self.img = cv2.imread(path)
        self.white_ranges = white_ranges
        if self.img is None:
            raise FileNotFoundError(f"画像が読み込めません: {path}")

    def get_white_area(self):
        lower, upper = self.white_ranges
        lower_white = np.array(lower)
        upper_white = np.array(upper)
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        area = cv2.countNonZero(mask)
        return area, mask