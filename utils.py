import os
from pynput import keyboard


scenes_to_load = []
scene_args = []
keyboard_checkers = []
listeners = []


def on_press(key: any) -> bool:
    for listener in keyboard_checkers:
        listener.on_press(key)
    return True


def on_release(key: any) -> bool:
    for listener in keyboard_checkers:
        listener.on_release(key)
    return True


def init_keyboard() -> None:
    listeners.append(keyboard.Listener(on_press=on_press, on_release=on_release))
    listeners[-1].start()


def close_keyboard() -> None:
    while len(listeners) > 0:
        listeners.pop(0).stop()
    keyboard_checkers.clear()


def get_terminal_size() -> tuple:
    try:
        return tuple(os.get_terminal_size())
    except OSError:
        return 80, 25


def pos(x: int, y: int) -> str:
    return f'\x1b[{y};{x}H'


def back(times: int = 1) -> str:
    return f'\033[{times}D'


def up(times: int = 1) -> str:
    return f'\033[{times}A'
