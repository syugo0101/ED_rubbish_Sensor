import cv2
import time
from picamera2 import Picamera2
import RPi.GPIO as GPIO
from pyzbar.pyzbar import decode
import os
import score_calculation

# ===== GPIO設定 =====
LED_PINS = [17, 27, 22]  # 任意のGPIOピン番号（BCM指定）
BUZZER_PIN = 4

GPIO.setmode(GPIO.BCM)
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# ===== json_path設定 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # このスクリプトのあるフォルダ
AREA_DATA_PATH = os.path.join(BASE_DIR, "area_data.json")

# ===== LED・ブザー通知 =====
def notify_success():
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.HIGH)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.LOW)

# ===== Webカメラ撮影 =====
def capture_from_webcam(save_dir="captures"):
    os.makedirs(save_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(save_dir, f"capture_{timestamp}.jpg")

    cap = cv2.VideoCapture(0)  # USBカメラが/dev/video0の場合
    if not cap.isOpened():
        raise RuntimeError("Webカメラが開けません")
    ret, frame = cap.read()
    cap.release()

    if ret:
        cv2.imwrite(save_path, frame)
        return frame, save_path
    else:
        raise RuntimeError("Webカメラ撮影失敗")

# ===== PiカメラでQRコード監視 =====
def watch_qr():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    last_detect_time = 0
    cooldown = 5  # 5秒間は同じQRコードを再検知しない

    try:
        while True:
            frame = picam2.capture_array()
            decoded = decode(frame)
            if decoded:
                qr_text = decoded[0].data.decode('utf-8')
                # area_x 形式かチェック
                if qr_text.startswith("area_") and time.time() - last_detect_time > cooldown:
                    area_key = qr_text
                    print(f"QRコード検出: {area_key}")

                    # Webカメラ撮影
                    img, path = capture_from_webcam()

                    # スコア計算
                    score = score_calculation.calculate_score(path, area_key, AREA_DATA_PATH)
                    print(f"算出スコア: {score}")
                    print(f"画像保存先: {path}")

                    # 通知
                    notify_success()

                    last_detect_time = time.time()

            time.sleep(0.1)  # CPU負荷軽減
    except KeyboardInterrupt:
        print("終了します...")
    finally:
        picam2.close()
        GPIO.cleanup()

# ===== 実行 =====
if __name__ == "__main__":
    watch_qr()
