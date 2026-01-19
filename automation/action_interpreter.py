import time
from utils.mac_window import resolve_window_rect, relative_to_absolute
from utils.mac_executor import mouse_click, input_text, press_key
from utils.screen_shot import capture_window


class ActionInterpreter:
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.window_rect = None

    def activate_and_capture(self):
        """激活应用（通过点击）并截图"""
        self.prepare()
        
        if self.window_rect:
            # 策略：点击窗口顶部中央（通常是标题栏），以激活窗口但不触发应用逻辑
            # x = 左 + 宽/2
            # y = 顶 + 10像素 (避开可能的菜单栏或边缘，但在标题栏范围内)
            # 注意：避开了左上角的红绿灯区域
            click_x = int(self.window_rect["x"] + self.window_rect["width"] / 2)
            click_y = int(self.window_rect["y"] + 10)
            
            print(f"Activating window by clicking safe area: ({click_x}, {click_y})")
            mouse_click(click_x, click_y)
            time.sleep(0.5) # 给一点时间让窗口获得焦点
            
            try:
                # 传入已获取的 window_rect，避免重复获取且避免 None 错误
                return capture_window(self.app_name, rect=self.window_rect)
            except Exception as e:
                print(f"Error capturing window: {e}")
                return None
        else:
            print("Failed to acquire window rect during activation.")
            return None

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