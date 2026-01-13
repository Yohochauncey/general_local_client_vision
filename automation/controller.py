from utils.screenshot import capture_screen
from backend.api import fetch_instruction
from automation.wx_controller import WeChatController


class AutomationController:
    def __init__(self):
        self.wx = WeChatController()

    def step(self):
        image = capture_screen()
        instruction = fetch_instruction(image)

        if instruction["target_app"] == "wechat":
            self.wx.execute(instruction["actions"])