import tkinter as tk
from backend.api import login
from ui.ui_main import MainWindow


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automation Login")
        self.root.geometry("300x150")

        tk.Label(self.root, text="Username").pack(pady=5)
        self.entry = tk.Entry(self.root)
        self.entry.pack()

        tk.Button(self.root, text="Login", command=self.on_login).pack(pady=20)

    def on_login(self):
        if login(self.entry.get()):
            self.root.destroy()
            MainWindow().run()

    def run(self):
        self.root.mainloop()