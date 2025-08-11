
import os
import cv2
import json
import count_write
import score_cal

# --- 定数・設定 ---
IMG_PLACE = "D:\\testimege\\"
IMG_LIST = [
    ["s1.jpg", "area_0"],
    ["s2.jpg", "area_0"]
]
AREA_DATA_PATH = "D:\\デスクトップ\\make\\ED\\ED_rubbish_Sensor\\image\\area_data.json"

# --- 関数 ---
def load_area_data(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def process_image(path, area_range, area_threshold):
    print("ファイル存在:", os.path.exists(path))
    counter = count_write.CountWhiteArea(path, area_range)
    white_area, white_mask = counter.get_white_area()
    print(f"白色領域の面積(ピクセル数): {white_area}", "area_threshold:", area_threshold)
    score_calculator = score_cal.ScoreCalculator(white_area, area_threshold)
    score = score_calculator.calculate_score(white_area, area_threshold)
    print(f"スコア: {score}")
    cv2.imshow("White Mask", white_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# --- メイン処理 ---
def main():
    area_data = load_area_data(AREA_DATA_PATH)
    for img_name, area_key in IMG_LIST:
        path = IMG_PLACE + img_name
        area_range = area_data[area_key]["range"]
        area_threshold = area_data[area_key]["threshold"]
        process_image(path, area_range, area_threshold)

if __name__ == "__main__":
    main()