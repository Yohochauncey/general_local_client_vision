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
    # kCGWindowListOptionOnScreenOnly: 仅屏幕上的窗口
    # kCGWindowListExcludeDesktopElements: 排除桌面元素
    options = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
    info = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

    candidates = []
    print(f"Searching windows for PID: {pid}")

    for w in info:
        if w.get("kCGWindowOwnerPID") == pid:
            bounds = w.get("kCGWindowBounds", {})
            width = bounds.get("Width", 0)
            height = bounds.get("Height", 0)
            layer = w.get("kCGWindowLayer", 0)
            
            # 过滤逻辑：
            # 1. 尺寸太小的通常不是主界面 (如 Tooltip, StatusItem 等)
            # if width < 200 or height < 200:
            #     continue
                
            # 2. Layer != 0 的通常是悬浮窗、菜单等，主窗口都在 Layer 0
            if layer != 0:
                continue
            
            candidates.append(w)
            print(f"Found candidate: ID={w.get('kCGWindowNumber')}, Size={width}x{height}, Name='{w.get('kCGWindowName')}'")

    if not candidates:
        print("No suitable window found.")
        return None
    
    # 按面积降序排序，取最大的通常是主窗口
    candidates.sort(key=lambda w: w.get("kCGWindowBounds", {}).get("Width", 0) * w.get("kCGWindowBounds", {}).get("Height", 0), reverse=True)
    
    best = candidates[0]
    b = best["kCGWindowBounds"]
    
    return {
        "x": b["X"],
        "y": b["Y"],
        "width": b["Width"],
        "height": b["Height"],
        "id": best.get("kCGWindowNumber"), # 关键：返回 Window ID
        "source": "quartz"
    }


def resolve_window_rect(app_name):
    pid = find_app_pid(app_name)
    print(pid)
    if not pid:
        raise RuntimeError("App 未运行")

    # rect = get_window_rect_ax(pid)
    # if rect:
    #     print("使用ax获取窗口")
    #     return rect

    rect = get_window_rect_quartz(pid)
    if rect:
        print("使用quartz获取窗口")
        return rect

    raise RuntimeError("无法解析窗口")


def relative_to_absolute(rect, rx, ry):
    return (
        rect["x"] + rect["width"] * rx,
        rect["y"] + rect["height"] * ry
    )
