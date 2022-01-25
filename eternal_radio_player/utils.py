import logging
import platform
import traceback
import miniaudio
import sounddevice

from ._version import __version__
from .exceptions import ResourceError


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


def pyside_version():
    try:
        import PySide6
    except ImportError:
        return None
    return PySide6.__version__


def qt_version():
    try:
        from PySide6.QtCore import qVersion
    except ImportError:
        return None
    return qVersion()


def system_info():
    return (
        f'Eternal Radio Player {__version__}\n'
        f'OS: {os_version()}\n'
        f'Python: {python_version()}\n'
        f'miniaudio: {miniaudio_version()}\n'
        f'miniaudio Backend: {miniaudio_backend_version()}\n'
        f'sounddevice: {sounddevice_version()}\n'
        f'sounddevice Backend: {sounddevice_backend_version()}\n'
        f'PySide: {pyside_version()}\n'
        f'Qt: {qt_version()}'
    )


def qt_resource(path, text=False):
    from PySide6 import QtCore

    file = QtCore.QFile(path)
    if text:
        is_open = file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text)
        file_wrapper = QtCore.QTextStream(file)
    else:
        is_open = file.open(QtCore.QIODevice.ReadOnly)
        file_wrapper = file
    if not is_open:
        raise ResourceError(f'{file.error()}: {file.errorString()}')
    data = file_wrapper.readAll()
    file.close()
    return data
