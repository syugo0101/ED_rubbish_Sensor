
import cv2
import os
import numpy as np
from count_area import CountArea

imglist = ["s1.jpg", "s2.jpg"]
cleannumber = 100000

# 白色のHSV範囲（調整可能）
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 30, 255])

counter = CountArea(lower_white, upper_white)

for i in imglist:
    path = "D:\\testimege\\" + i
    print("ファイル存在:", os.path.exists(path))

    img = cv2.imread(path)
    print("読み込み結果:", type(img), "shape:" if img is not None else "None")

    if img is None:
        raise FileNotFoundError(f"画像が読み込めません: {path}")

    white_area, white_mask = counter.get_white_area(img)
    print("白色領域の面積(ピクセル数):", white_area)

    if white_area > cleannumber:
        print(i, "切子が多い")
    else:
        print(i, "切子が少ない")