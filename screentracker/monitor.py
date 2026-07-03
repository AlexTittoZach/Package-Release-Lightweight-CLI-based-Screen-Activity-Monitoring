import win32gui
import win32process
import psutil


def get_active_window():

    hwnd = win32gui.GetForegroundWindow()

    title = win32gui.GetWindowText(hwnd)

    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        process = psutil.Process(pid)

        return {
            "app": process.name(),
            "title": title
        }

    except:
        return {
            "app": "Unknown",
            "title": ""
        }