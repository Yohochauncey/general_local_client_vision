import tkinter as tk
from automation.wx_controller import WeChatController


class OverlayWindow:
    def __init__(self, app_name):
        self.controller = WeChatController(app_name)

        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.geometry("220x50+600+0")
        self.root.attributes("-topmost", True)

        tk.Label(
            self.root,
            text="🟢 屏幕控制中",
            bg="black",
            fg="white"
        ).pack(fill="both", expand=True)

        tk.Button(self.root, text="结束", command=self.stop).pack(fill="both")

    def stop(self):
        self.controller.stop()
        self.root.destroy()
