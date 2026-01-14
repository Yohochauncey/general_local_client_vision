import tkinter as tk
from backend.heartbeat import start_heartbeat
from ui.ui_overlay import OverlayWindow


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automation Client")
        self.root.geometry("400x200")

        self.app = tk.StringVar(value="WeChat")

        tk.Label(self.root, text="选择应用").pack()
        tk.OptionMenu(self.root, self.app, "WeChat").pack()

        tk.Button(self.root, text="开始自动化", command=self.start).pack(pady=40)

    def start(self):
        start_heartbeat()
        self.root.withdraw()
        OverlayWindow(self.app.get())

    def run(self):
        self.root.mainloop()
