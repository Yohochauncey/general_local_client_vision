from PIL import ImageGrab
import subprocess
from utils.mac_window import resolve_window_rect


def capture_screen(path="screen.png"):
    img = ImageGrab.grab()
    img.save(path)
    return path


def capture_window(app_name, path="wechat_screenshot.png", rect=None):
    try:
        # 1. 优先尝试使用 Window ID 进行精确截图 (screencapture -l)
        if rect and rect.get("id"):
            window_id = rect["id"]
            print(f"Attempting capture with Window ID: {window_id}")
            try:
                # -x: 不播放声音
                # -l: 指定 Window ID
                # -o: 不带窗口阴影 (可选，如果只要内容可以加，这里先不加，保持原样)
                subprocess.run(["screencapture", "-x", "-l", str(window_id), path], check=True)
                print(f"Screenshot saved to {path} using Window ID {window_id}")
                return path
            except subprocess.CalledProcessError as e:
                print(f"screencapture command failed: {e}, falling back to PIL...")
        
        # 2. 回退方案：使用坐标截图 (PIL ImageGrab)
        # 注意：macOS Retina 屏幕上，ImageGrab 可能需要 x2 坐标，或者系统自动处理
        # 如果 Window ID 失败，可能是权限问题，坐标截图可能也面临背景问题，但作为最后手段
        if rect:
            x = int(rect["x"])
            y = int(rect["y"])
            width = int(rect["width"])
            height = int(rect["height"])
            
            print(f"Fallback to PIL grab: region ({x}, {y}, {width}, {height})")
            img = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            img.save(path)
            print(f"Screenshot saved to {path} (Region: {x},{y},{width},{height})")
            return path
            
        print("No rect provided for capture.")
        return None

    except Exception as e:
        print(f"Failed to capture window for {app_name}: {e}")
        return None