from PyQt5 import QtWidgets, QtCore
import sys
import backend.api


class LoginWindow(QtWidgets.QWidget):
    login_success = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录")
        self.setFixedSize(300, 180)

        layout = QtWidgets.QVBoxLayout(self)

        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText("请输入用户名")
        self.login_btn = QtWidgets.QPushButton("登录")

        layout.addWidget(self.username)
        layout.addWidget(self.login_btn)

        self.login_btn.clicked.connect(self.handle_login)

    def handle_login(self):
        name = self.username.text().strip()
        if not name:
            return

        user = self.api.login(name)
        if user:
            self.login_success.emit(user)
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "登录失败", "用户名无效")