import threading, time, requests


class Heartbeat(threading.Thread):
    def __init__(self, client_id):
        super().__init__()
        self.client_id = client_id
        self.daemon = True

    def run(self):
        while True:
            try:
                requests.post("http://your-backend/api/heartbeat", json={"client_id": self.client_id})
            except:
                pass
            time.sleep(10)