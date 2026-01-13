import Quartz
from AppKit import NSWorkspace

def find_app_by_name(name):
    for app in NSWorkspace.sharedWorkspace().runningApplications():
        if name.lower() in app.localizedName().lower():
            return app.processIdentifier()
    return None


def ax_click(pid, x, y):
    event = Quartz.CGEventCreateMouseEvent(
        None,
        Quartz.kCGEventLeftMouseDown,
        Quartz.CGPoint(x, y),
        Quartz.kCGMouseButtonLeft
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    event = Quartz.CGEventCreateMouseEvent(
        None,
        Quartz.kCGEventLeftMouseUp,
        Quartz.CGPoint(x, y),
        Quartz.kCGMouseButtonLeft
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)


def ax_input(text):
    for c in text:
        event = Quartz.CGEventCreateKeyboardEvent(None, 0, True)
        Quartz.CGEventKeyboardSetUnicodeString(event, 1, c)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)


def capture_screen():
    image = Quartz.CGWindowListCreateImage(
        Quartz.CGRectInfinite,
        Quartz.kCGWindowListOptionOnScreenOnly,
        Quartz.kCGNullWindowID,
        Quartz.kCGWindowImageDefault
    )
    return image