import spidev
import RPi.GPIO as GPIO
from adafruit_rgb_display import ili9341
from PIL import Image, ImageDraw, ImageFont
import time

# 手動でピン番号指定

# SPI設定
SPI_PORT = 0           # SPI0
SPI_DEVICE = 0         # CE0
SPI_MODE = 0           # SPIモード0
SPI_BITS_PER_WORD = 8  # 8bit
SPI_MAX_SPEED_HZ = 32000000  # 32MHz

# 各ピンの基板上の表示
CS_PIN = 8      # GPIO8 (CE0)   : SPI チップセレクト (CS)
DC_PIN = 25     # GPIO25        : LCD データ/コマンド (DC)
RESET_PIN = 23  # GPIO23        : LCD リセット (RESET)
BACKLIGHT_PIN = 24 # GPIO24      : LCD バックライト (BL)


print('GPIO初期化...')
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_PIN, GPIO.OUT)
GPIO.setup(DC_PIN, GPIO.OUT)
GPIO.setup(RESET_PIN, GPIO.OUT)
GPIO.setup(BACKLIGHT_PIN, GPIO.OUT)
print(f'CS_PIN={CS_PIN}, DC_PIN={DC_PIN}, RESET_PIN={RESET_PIN}, BACKLIGHT_PIN={BACKLIGHT_PIN}')
print(f'初期ピン状態: CS={GPIO.input(CS_PIN)}, DC={GPIO.input(DC_PIN)}, RESET={GPIO.input(RESET_PIN)}, BL={GPIO.input(BACKLIGHT_PIN)}')


print('SPI手動設定...')
spi = spidev.SpiDev()
spi.open(SPI_PORT, SPI_DEVICE)
spi.mode = SPI_MODE
spi.bits_per_word = SPI_BITS_PER_WORD
spi.max_speed_hz = SPI_MAX_SPEED_HZ
print(f'SPI_PORT={SPI_PORT}, SPI_DEVICE={SPI_DEVICE}, MODE={SPI_MODE}, BITS={SPI_BITS_PER_WORD}, SPEED={SPI_MAX_SPEED_HZ}')
print(f'SPI状態: opened={spi.fd is not None}, mode={spi.mode}, bits={spi.bits_per_word}, speed={spi.max_speed_hz}')


print('LCDリセット処理...')
GPIO.output(RESET_PIN, GPIO.LOW)
print(f'リセットピン LOW: {GPIO.input(RESET_PIN)}')
time.sleep(0.5)
GPIO.output(RESET_PIN, GPIO.HIGH)
print(f'リセットピン HIGH: {GPIO.input(RESET_PIN)}')
time.sleep(0.5)
print('reset ok')


print('adafruit_rgb_displayピンラッパー作成...')
class PinWrap:
	def __init__(self, pin):
		self.pin = pin
		GPIO.setup(pin, GPIO.OUT)
	def value(self, v=None):
		if v is None:
			return GPIO.input(self.pin)
		GPIO.output(self.pin, GPIO.HIGH if v else GPIO.LOW)

cs_pin = PinWrap(CS_PIN)
dc_pin = PinWrap(DC_PIN)
reset_pin = PinWrap(RESET_PIN)

print('ILI9341ディスプレイ初期化...')
try:
	display = ili9341.ILI9341(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=SPI_MAX_SPEED_HZ)
	print('ILI9341初期化成功')
except Exception as e:
	print(f'ILI9341初期化失敗: {e}')

GPIO.output(BACKLIGHT_PIN, GPIO.HIGH)
print(f'backlight on: {GPIO.input(BACKLIGHT_PIN)}')


if 'display' in locals():
	print(f'Display size: {display.width}x{display.height}')
	print('画像生成...')
	image = Image.new("RGB", (display.width, display.height))
	draw = ImageDraw.Draw(image)
	font = ImageFont.load_default()
	draw.text((10, 10), "Hello", font=font, fill=(255, 255, 255))
	print('画像描画...')
	try:
		display.image(image)
		print('image print ok')
	except Exception as e:
		print(f'画像描画エラー: {e}')
else:
	print('ディスプレイ初期化失敗のため画像描画スキップ')

time.sleep(10)

print('バックライトOFF')
GPIO.output(BACKLIGHT_PIN, GPIO.LOW)
print(f'backlight off: {GPIO.input(BACKLIGHT_PIN)}')
GPIO.cleanup()