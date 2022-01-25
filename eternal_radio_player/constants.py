from ._version import __version__


CREDITS = (
    'Eternal Radio Player\n'
    'License: GPLv3+ - https://github.com/alexitx/eternal-radio-player/blob/master/LICENSE\n'
    '---\n'
    'numpy - https://github.com/numpy/numpy\n'
    'License: BSD 3-Clause - https://github.com/numpy/numpy/blob/main/LICENSE.txt\n'
    '---\n'
    'platformdirs - https://github.com/platformdirs/platformdirs\n'
    'License: MIT - https://github.com/platformdirs/platformdirs/blob/main/LICENSE.txt\n'
    '---\n'
    'pyminiaudio - https://github.com/irmen/pyminiaudio\n'
    'License: MIT - https://github.com/irmen/pyminiaudio/blob/master/LICENSE\n'
    '---\n'
    'python-sounddevice - https://github.com/spatialaudio/python-sounddevice\n'
    'License: MIT - https://github.com/spatialaudio/python-sounddevice/blob/master/LICENSE\n'
    '---\n'
    'requests - https://github.com/psf/requests\n'
    'License: Apache 2.0 - https://github.com/psf/requests/blob/main/LICENSE\n'
    '---\n'
    'schema - https://github.com/keleshev/schema\n'
    'License: MIT - https://github.com/keleshev/schema/blob/master/LICENSE-MIT\n'
    '---\n'
    'timeago - https://github.com/hustcc/timeago\n'
    'License: MIT - https://github.com/hustcc/timeago/blob/master/LICENSE\n'
    '---\n'
    'PyQtDarkTheme - https://github.com/5yutan5/PyQtDarkTheme\n'
    'License: MIT - https://github.com/5yutan5/PyQtDarkTheme/blob/main/LICENSE.txt\n'
    '---\n'
    'PySide6 - https://wiki.qt.io/Qt_for_Python\n'
    'License: LGPLv3 - https://tldrlegal.com/license/gnu-lesser-general-public-license-v3-(lgpl-3)\n'
    '---\n'
    'RemixIcon - https://github.com/Remix-Design/RemixIcon\n'
    'License: Apache 2.0 - https://github.com/Remix-Design/RemixIcon/blob/master/License'
)

USER_AGENT = f'Eternal Radio Player/{__version__}'
REQUEST_TIMEOUT = 5.0

STREAM_URL = 'https://radio.jump.bg/proxy/mnikolov/stream'
STREAM_ITER_CHUNK_SIZE = 16 * 1024

PLAYER_FRAME_COUNT = 4 * 1024

RECENT_SONGS_URL = 'https://radio.jump.bg/recentfeed/mnikolov/json'
RECENT_SONGS_CACHE_TIME = 10.0

CONFIG_DEFAULTS = {
    'connection-timeout': REQUEST_TIMEOUT,
    'volume': 1.0
}
