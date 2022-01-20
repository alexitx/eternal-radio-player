import logging
import platform
import sys
import traceback
import miniaudio
import sounddevice
from pathlib import Path

from ._version import __version__


log = logging.getLogger(__name__)


def format_exc(exc, tb=False):
    if str(exc):
        msg = f'{type(exc).__name__}: {exc}'
        if tb:
            return f'{msg}\n{traceback.format_exc()}'
        return msg
    return f'{type(exc).__name__}: {traceback.format_exc()}'


def os_version():
    if platform.system() == 'Windows':
        return f'{platform.platform()} {platform.machine()}'
    return platform.platform()


def python_version():
    return f'{platform.python_implementation()} {platform.python_version()} [{platform.python_compiler()}]'


def miniaudio_version():
    return miniaudio.__version__


def miniaudio_backend_version():
    return miniaudio.lib_version()


def sounddevice_version():
    return sounddevice.__version__


def sounddevice_backend_version():
    return sounddevice.get_portaudio_version()[1]


def system_info():
    return (
        f'Eternal Radio Player {__version__}\n'
        f'OS: {os_version()}\n'
        f'Python: {python_version()}\n'
        f'miniaudio: {miniaudio_version()}\n'
        f'miniaudio Backend: {miniaudio_backend_version()}\n'
        f'sounddevice: {sounddevice_version()}\n'
        f'sounddevice Backend: {sounddevice_backend_version()}'
    )
