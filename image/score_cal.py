# スコアを最大10000点として計算
import math

max_score = 10000
amount_of_change = math.e

class ScoreCalculator:
    def __init__(self, pixcel, area_threshold):
        self.pixcel = pixcel
        self.area_threshold = area_threshold

    def calculate_score(self, white_area, area_threshold):
        if white_area <=area_threshold:
            return max_score
        else:
            score = max_score * amount_of_change ** (-white_area/area_threshold)
            return score