import cv2
import numpy as np
import json
import math

# スコアを最大10000点として計算
max_score = 10000
amount_of_change = math.e


class ScoreCalculator:
    def __init__(self, path, area ,area_path):
        self.path = path
        self.area = area
        self.area_path = area_path

    def load_area_data(self):
        with open(self.area_path, "r") as f:
            return json.load(f)
    
    def calculate_score(self):
        area_data = self.load_area_data()

        area_range = area_data[self.area]["range"]
        area_threshold = area_data[self.area]["threshold"]

        counter = CountWhiteArea(self.path, area_range)
        white_area = counter.get_white_area()

        score = Score(white_area, area_threshold)
        return score.score()

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
        return area
    
class Score:
    def __init__(self, pixel, area_threshold):
        self.pixel = pixel
        self.area_threshold = area_threshold

    def score(self):
        if self.pixel <= self.area_threshold:
            return max_score
        else:
            score = max_score * amount_of_change ** (-self.pixel/self.area_threshold)
            return score