import win32gui
import win32con
import win32api


class Win32Window:
    def __init__(self, title=None, class_name=None):
        self.hwnd = None
        self.title = title
        self.class_name = class_name

    def find(self):
        """根据标题或类名查找窗口"""
        def callback(hwnd, extra):
            if self.title and self.title in win32gui.GetWindowText(hwnd):
                self.hwnd = hwnd
            elif self.class_name:
                try:
                    cls = win32gui.GetClassName(hwnd)
                    if cls == self.class_name:
                        self.hwnd = hwnd
                except:
                    pass
            return True

        win32gui.EnumWindows(callback, None)
        return self.hwnd

    def get_client_rect(self):
        """
        获取 client 区域（不含标题栏）的绝对坐标
        """
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        client_left, client_top = win32gui.ClientToScreen(self.hwnd, (0, 0))
        return {
            "left": client_left,
            "top": client_top,
            "width": right - left,
            "height": bottom - top
        }

    def click_client(self, x, y):
        """
        在 client 区域内后台点击，不移动鼠标
        """
        lParam = win32api.MAKELONG(int(x), int(y))

        # 鼠标按下+抬起
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, None, lParam)

    def send_text(self, text):
        """后台输入文本（SendMessage，不抢焦点）"""
        for ch in text:
            win32api.SendMessage(self.hwnd, win32con.WM_CHAR, ord(ch), 0)