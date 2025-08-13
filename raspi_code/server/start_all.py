import subprocess
import time
import signal

def main():
    app_proc = subprocess.Popen(['python3', 'app.py'])
    print("app.py started")

    ble_proc = subprocess.Popen(['node', 'ble_server.js'])
    print("ble_server.js started")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("終了処理中...")
        app_proc.send_signal(signal.SIGINT)
        ble_proc.send_signal(signal.SIGINT)
        app_proc.wait()
        ble_proc.wait()
        print("終了しました。")

if __name__ == '__main__':
    main()