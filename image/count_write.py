
import cv2
import numpy as np

# エリア番号ごとに白色範囲を切り替え可能
white_ranges = [
    ([0, 0, 200], [180, 30, 255]),  # 0: 標準
    ([0, 0, 200], [190, 30, 255]),  # 1: 広め
    ([0, 0, 220], [180, 20, 255])   # 2: 狭め（例）
]

class CountWhiteArea:
    def __init__(self, path, areanum=0):
        self.img = cv2.imread(path)
        self.areanum = areanum
        if self.img is None:
            raise FileNotFoundError(f"画像が読み込めません: {path}")

    def get_white_area(self):
        lower, upper = white_ranges[self.areanum]
        lower_white = np.array(lower)
        upper_white = np.array(upper)
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        area = cv2.countNonZero(mask)
        return area, mask