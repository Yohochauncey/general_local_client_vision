import Quartz
from utils.mac_app import find_app_pid


def get_window_rect_ax(pid):
    try:
        app = Quartz.AXUIElementCreateApplication(pid)
        err, wins = Quartz.AXUIElementCopyAttributeValue(
            app, "AXWindows", None
        )
        if err != 0 or not wins:
            return None

        win = wins[0]
        _, pos = Quartz.AXUIElementCopyAttributeValue(win, "AXPosition", None)
        _, size = Quartz.AXUIElementCopyAttributeValue(win, "AXSize", None)

        return {
            "x": pos.x,
            "y": pos.y,
            "width": size.width,
            "height": size.height,
            "source": "ax"
        }
    except Exception:
        return None


def get_window_rect_quartz(pid):
    info = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly,
        Quartz.kCGNullWindowID
    )

    for w in info:
        if w.get("kCGWindowOwnerPID") == pid:
            b = w["kCGWindowBounds"]
            return {
                "x": b["X"],
                "y": b["Y"],
                "width": b["Width"],
                "height": b["Height"],
                "source": "quartz"
            }
    return None


def resolve_window_rect(app_name):
    pid = find_app_pid(app_name)
    print(pid)
    if not pid:
        raise RuntimeError("App 未运行")

    rect = get_window_rect_ax(pid)
    if rect:
        return rect

    rect = get_window_rect_quartz(pid)
    if rect:
        return rect

    raise RuntimeError("无法解析窗口")


def relative_to_absolute(rect, rx, ry):
    return (
        rect["x"] + rect["width"] * rx,
        rect["y"] + rect["height"] * ry
    )
