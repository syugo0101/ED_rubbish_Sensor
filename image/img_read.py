import count_write
import os
import cv2
import json
import score_cal

# 画像データを仮置き
imgplace = "D:\\testimege\\"
imglist = [["s1.jpg","area_0"], ["s2.jpg","area_0"]]

# jsonでarea_data管理(白色のレンジ,閾値)
with open("D:\\デスクトップ\\make\\ED\\ED_rubbish_Sensor\\image\\area_data.json", "r") as f:
    area_data = json.load(f)

for i in imglist:
    area_threshold = area_data[i[1]]["threshold"]
    path = imgplace + i[0]
    print("ファイル存在:", os.path.exists(path))
    counter = count_write.CountWhiteArea(path, area_data[i[1]]["range"])
    white_area, white_mask = counter.get_white_area()
    print(f"白色領域の面積(ピクセル数): {white_area}", "area_threshold:", area_threshold)

    score_calculator = score_cal.ScoreCalculator(white_area, area_threshold)
    score = score_calculator.calculate_score(white_area, area_threshold)
    print(f"スコア: {score}")

    cv2.imshow("White Mask", white_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()