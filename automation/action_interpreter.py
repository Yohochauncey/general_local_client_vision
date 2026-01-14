import time
from utils.mac_window import resolve_window_rect, relative_to_absolute
from utils.mac_executor import mouse_click, input_text, press_key


class ActionInterpreter:
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.window_rect = None

    def prepare(self):
        self.window_rect = resolve_window_rect(self.app_name)

    def execute(self, actions):
        self.prepare()
        for step in actions:
            self.execute_step(step)
            time.sleep(0.2)

    def execute_step(self, step):
        t = step["type"]

        if t == "click":
            x, y = relative_to_absolute(self.window_rect, step["rx"], step["ry"])
            mouse_click(x, y)

        elif t == "input":
            input_text(step["text"])

        elif t == "key":
            press_key(step["key"])

        else:
            raise ValueError(f"未知 action: {t}")