import cv2
import time
from picamera2 import Picamera2
import RPi.GPIO as GPIO
from pyzbar.pyzbar import decode
import os
import score_calculation
import json

# ===== GPIO設定 =====
LED_PINS = [17, 27, 22]
BUZZER_PIN = 4

GPIO.setmode(GPIO.BCM)
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# ===== json_path設定 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AREA_DATA_PATH = os.path.join(BASE_DIR, "area_data.json")

# スコア保存用ファイルパス（Node.jsが読む想定）
SCORE_DATA_PATH = os.path.join(BASE_DIR, "score_data.json")

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

    cap = cv2.VideoCapture(0)
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
    ALL_AREAS = {"area_0", "area_1", "area_2"}  # 対象エリアセット（必要に応じて変更）

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    captured_areas = set()
    current_scores = {}

    last_detect_time = 0
    cooldown = 5  # 同じQRコードの再検知間隔(秒)

    try:
        while True:
            frame = picam2.capture_array()
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            decoded = decode(gray)
            if decoded:
                qr_text = decoded[0].data.decode('utf-8')
                if qr_text.startswith("area_") and time.time() - last_detect_time > cooldown:
                    area_key = qr_text
                    if area_key in captured_areas:
                        time.sleep(0.1)
                        continue

                    print(f"QRコード検出: {area_key}")

                    picam2.stop()

                    try:
                        img, path = capture_from_webcam()
                    except RuntimeError as e:
                        print(e)
                        picam2.start()
                        continue

                    calscore = score_calculation.ScoreCalculator(path, area_key, AREA_DATA_PATH)
                    score = calscore.calculate_score()
                    print(f"算出スコア: {score}")
                    print(f"画像保存先: {path}")

                    notify_success()

                    current_scores[area_key] = score
                    captured_areas.add(area_key)

                    # 全エリアのスコアが揃ったらファイルに保存
                    MAX_SET_COUNT = 10
                    MAX_IMAGE_COUNT = 9
                    CAPTURE_DIR = "captures"

                    if captured_areas == ALL_AREAS:
                        # 既存のスコアを読み込み
                        if os.path.exists(SCORE_DATA_PATH):
                            with open(SCORE_DATA_PATH, "r", encoding="utf-8") as f:
                                try:
                                    existing_scores = json.load(f)
                                except json.JSONDecodeError:
                                    existing_scores = {}
                        else:
                            existing_scores = {}

                        # タイムスタンプ付きで保存
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        existing_scores[timestamp] = current_scores

                        # 最大10セットまで保持
                        sorted_keys = sorted(existing_scores.keys())
                        while len(sorted_keys) > MAX_SET_COUNT:
                            oldest = sorted_keys.pop(0)
                            del existing_scores[oldest]

                        # JSON書き込み
                        with open(SCORE_DATA_PATH, "w", encoding="utf-8") as f:
                            json.dump(existing_scores, f, ensure_ascii=False, indent=2)

                        # 画像の古いものを削除
                        os.makedirs(CAPTURE_DIR, exist_ok=True)
                        images = sorted(
                            [os.path.join(CAPTURE_DIR, fn) for fn in os.listdir(CAPTURE_DIR)],
                            key=lambda x: os.path.getmtime(x)
                        )
                        while len(images) > MAX_IMAGE_COUNT:
                            os.remove(images.pop(0))

                        print(f"スコアセット完成: {json.dumps(current_scores, ensure_ascii=False)}")
                        captured_areas.clear()
                        current_scores.clear()

                    last_detect_time = time.time()

                    picam2.start()

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("終了します...")
    finally:
        picam2.close()
        GPIO.cleanup()

if __name__ == "__main__":
    watch_qr()