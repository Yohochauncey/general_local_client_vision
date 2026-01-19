import threading
import time
from backend.api import fetch_action
from automation.action_interpreter import ActionInterpreter


class WeChatController:
    def __init__(self, app_name):
        self.interpreter = ActionInterpreter(app_name)
        self.running = True
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        # 初始化：激活应用并截图 (逻辑已移至 Interpreter)
        self.interpreter.activate_and_capture()

        while self.running:
            time.sleep(2)
            task = fetch_action()
            if task:
                self.interpreter.execute(task["actions"])
            time.sleep(2)

    def stop(self):
        self.running = False
