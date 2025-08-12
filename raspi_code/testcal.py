import os
import score_calculation

# スコア算出の流れを確認するための仮のもの

# --- 定数・設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # このスクリプトのあるフォルダ
IMG_PLACE = os.path.join(BASE_DIR, "testimages//")  # imagesフォルダ
IMG_LIST = [
    ["s1.jpg", "area_0"],
    ["s2.jpg", "area_0"]
]
AREA_DATA_PATH = os.path.join(BASE_DIR, "area_data.json")  # JSONファイル

def main():
    for i in IMG_LIST:
        img_name, area_key = i
        path = os.path.join(IMG_PLACE, img_name)
        score_calculator = score_calculation.ScoreCalculator(path, area_key, AREA_DATA_PATH)
        try:
            score = score_calculator.calculate_score()
            print(f"画像: {img_name}, スコア: {score}")
        except Exception as e:
            print(f"画像: {img_name} の処理中にエラーが発生しました: {e}")

if __name__ == "__main__":
    main()