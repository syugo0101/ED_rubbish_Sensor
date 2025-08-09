import cv2
import numpy as np

# バージョン確認
print("OpenCV version:", cv2.__version__)

# 100x100 の青い画像を作成
img = np.zeros((100, 100, 3), dtype=np.uint8)
img[:] = (255, 0, 0)  # 青 (BGR)

# 画面に表示
cv2.imshow("Blue Square", img)
cv2.waitKey(0)
cv2.destroyAllWindows()