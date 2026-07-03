import ctypes


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("dwTime", ctypes.c_uint)
    ]


def get_idle_seconds():

    last_input = LASTINPUTINFO()

    last_input.cbSize = ctypes.sizeof(
        LASTINPUTINFO
    )

    ctypes.windll.user32.GetLastInputInfo(
        ctypes.byref(last_input)
    )

    millis = (
        ctypes.windll.kernel32.GetTickCount()
        - last_input.dwTime
    )

    return millis / 1000.0