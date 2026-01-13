from utils.mac_ax_helper import find_app_by_name, ax_click, ax_input


class WeChatController:
    def execute(self, actions):
        pid = find_app_by_name("WeChat")
        if not pid:
            return

        for act in actions:
            if act["type"] == "click":
                ax_click(pid, act["x"], act["y"])
            elif act["type"] == "input":
                ax_input(act["text"])
