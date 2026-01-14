import threading
import time


def start_heartbeat():
    def loop():
        while True:
            print("[HEARTBEAT]")
            time.sleep(5)

    threading.Thread(target=loop, daemon=True).start()