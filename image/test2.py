import os

path = r"D:\デスクトップ\make\ED\ED_rubbish_Sensor\image\s_1.jpg"

if not os.path.isfile(path):
    print("ファイルが存在しません。パスを確認してください。")
else:
    print("ファイルは存在します。")