from PIL import Image

path = r"D:\デスクトップ\make\ED\ED_rubbish_Sensor\image\s_1.jpg"

try:
    img_pil = Image.open(path)
    img_pil.show()
    print("PILで画像読み込み成功")
except Exception as e:
    print("PILでの画像読み込みに失敗:", e)