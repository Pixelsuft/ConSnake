import os
import ctypes
import platform
import defines


system_dir_name = platform.system().lower()
use_l = False
l_str = 'L' if use_l else ''
if system_dir_name == 'darwin':
    raise OSError('MacOS Sucks!')
elif system_dir_name == 'windows':
    translates = {
        'amd64': 'x64',
        'i386': 'x86'
    }
    arch_dir_name = translates.get(platform.machine().lower())
    if not arch_dir_name:
        raise OSError(f'No Support For {arch_dir_name.title()} Yet!')
    os.environ['FMOD_LIBRARY_PATH'] = f'fmod{l_str}.dll'
    ctypes.windll.LoadLibrary(os.path.join(
        defines.CWD,
        'fmod',
        'windows',
        arch_dir_name,
        os.getenv('FMOD_LIBRARY_PATH')
    ))
elif system_dir_name == 'linux':
    arch_dir_name = platform.machine().lower()
    if arch_dir_name in ('i386', 'i686'):
        arch_dir_name = 'x86'
    elif arch_dir_name == 'x64':
        arch_dir_name = 'x86_64'
    if arch_dir_name not in ('arm', 'arm64', 'x86', 'x86_64'):
        raise OSError(f'No Support For {arch_dir_name.title()} Yet!')
    os.environ['FMOD_LIBRARY_PATH'] = f'libfmod{l_str}.so'
    ctypes.CDLL(os.path.join(
        defines.CWD,
        'fmod',
        'linux',
        arch_dir_name,
        os.getenv('FMOD_LIBRARY_PATH')
    ))
else:
    raise OSError(f'No Support For {system_dir_name.title()} Yet!')


try:
    import pyfmodex
    from pyfmodex.flags import MODE
except Exception as _err:
    raise RuntimeError(f'Failed To Load FMOD: {_err}')


sound_system = pyfmodex.System()
SOUND_MODE = MODE.DEFAULT
