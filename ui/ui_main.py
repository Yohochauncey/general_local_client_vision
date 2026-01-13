# ui_main.py
from PyQt5 import QtWidgets, QtCore
from backend.heartbeat import Heartbeat
from ui_overlay import OverlayWindow

class MainWindow(QtWidgets.QWidget):
    start_automation = QtCore.pyqtSignal()

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info

        self.setWindowTitle("桌面自动化客户端")
        self.setFixedSize(400, 300)

        layout = QtWidgets.QVBoxLayout(self)

        self.app_combo = QtWidgets.QComboBox()
        self.app_combo.addItems(["微信"])  # 可扩展

        self.start_btn = QtWidgets.QPushButton("开始自动化")
        layout.addWidget(self.app_combo)
        layout.addWidget(self.start_btn)

        self.start_btn.clicked.connect(self.handle_start)

        # 启动心跳
        self.heartbeat = Heartbeat(user_info["user_id"])
        self.heartbeat.start()

    def handle_start(self):
        self.hide()
        self.overlay = OverlayWindow()
        self.overlay.show()
        self.start_automation.emit()