import ctypes
import atexit
import colorama
import utils
import main_menu
from fmod_loader import sound_system


if hasattr(ctypes, 'windll'):
    ctypes.windll.kernel32.SetConsoleTitleW('Pixelsuft ConSnake')
colorama.init()
sound_system.init()
utils.init_keyboard()
atexit.register(sound_system.close)
atexit.register(utils.close_keyboard)

utils.scenes_to_load.append(main_menu.MainMenu)

while len(utils.scenes_to_load) > 0:
    utils.scenes_to_load.pop(0)(*utils.scene_args)
