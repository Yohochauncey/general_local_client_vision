import subprocess


def find_app_pid(app_name: str):
    try:
        out = subprocess.check_output(
            ["pgrep", "-f", app_name]
        )
        return int(out.splitlines()[0])
    except Exception:
        return None