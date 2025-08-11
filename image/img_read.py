import count_write
import os
import cv2

imgplace = "D:\\testimege\\"
imglist = [["s1.jpg",0], ["s2.jpg",0]]
area_threshold = 100000

for i in imglist:
    path = imgplace + i[0]
    print("ファイル存在:", os.path.exists(path))
    counter = count_write.CountWhiteArea(path, i[1])
    white_area, white_mask = counter.get_white_area()
    print(f"白色領域の面積(ピクセル数): {white_area}")
    if white_area > area_threshold:
        print(i[0], "切子が多い")
    else:
        print(i[0], "切子が少ない")
    cv2.imshow("White Mask", white_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()