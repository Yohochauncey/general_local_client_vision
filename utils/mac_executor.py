import Quartz
import time


def mouse_click(x, y):
    pt = Quartz.CGPoint(x, y)
    for ev_type in (
        Quartz.kCGEventLeftMouseDown,
        Quartz.kCGEventLeftMouseUp
    ):
        ev = Quartz.CGEventCreateMouseEvent(
            None, ev_type, pt, Quartz.kCGMouseButtonLeft
        )
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, ev)
        time.sleep(0.01)


def input_text(text):
    for ch in text:
        ev = Quartz.CGEventCreateKeyboardEvent(None, 0, True)
        Quartz.CGEventKeyboardSetUnicodeString(ev, 1, ch)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, ev)
        time.sleep(0.02)


KEY_MAP = {"enter": 36}


def press_key(key):
    code = KEY_MAP[key]
    for down in (True, False):
        ev = Quartz.CGEventCreateKeyboardEvent(None, code, down)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, ev)
