import ctypes
import pyautogui

# Флаг для перемещения мыши
MOUSEEVENTF_MOVE = 0x0001

# Класс для того, чтобы упаковывать информацию для ctypes
class INPUT(ctypes.Structure):
    class _INPUTunion(ctypes.Union):
        class _MOUSEINPUT(ctypes.Structure):
            _fields_ = [
                ("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
            ]
        _fields_ = [
            ("mi", _MOUSEINPUT)
        ]
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("u", _INPUTunion)
    ]

def moveMouse (dx: int, dy: int) -> None:
    '''Двигает мшыку через сырые данные.'''
    inputs = INPUT(type = 0)
    inputs.mi.dx = dx
    inputs.mi.dy = dy
    inputs.mi.dwFlags = MOUSEEVENTF_MOVE

    ctypes.windll.user32.SendInput(1, ctypes.byref(inputs), ctypes.sizeof(inputs))

def moveMouseEvent (key: str, step: int) -> None:
    '''Ивент - считывает нажатую клавишу (стрелочки) и двигает камеру в соотв. направлении на заданное количество пикселей (step).'''
    if key == 'up':
        moveMouse(0, -step)
    elif key == 'down':
        moveMouse(0, step)
    elif key == 'left':
        moveMouse(-step, 0)
    elif key == 'right':
        moveMouse(step, 0)

def clickMouseEvent (key: str, type: str) -> None:
    '''Ивент - считывает нажатую клавишу (ctrl, alt) и кликает соотв. кнопку мыши.'''
    if key == 'ctrl':
        if type == 'down':
            pyautogui.mouseDown(button='left')
        elif type == 'up':
            pyautogui.mouseUp(button='left')
    elif key == 'alt':
        if type == 'down':
            pyautogui.mouseDown(button='right')
        elif type == 'up':
            pyautogui.mouseUp(button='right')