from ._version import __version__


CREDITS = (
    'Eternal Radio Player\n'
    'License: GNU General Public License v3.0 or later - https://github.com/alexitx/eternal-radio-player/blob/master/LICENSE\n'
    '---\n'
    'pyminiaudio - https://github.com/irmen/pyminiaudio\n'
    'License: MIT - https://github.com/irmen/pyminiaudio/blob/master/LICENSE\n'
    '---\n'
    'numpy - https://github.com/numpy/numpy\n'
    'License: BSD 3-Clause - https://github.com/numpy/numpy/blob/main/LICENSE.txt\n'
    '---\n'
    'requests - https://github.com/psf/requests\n'
    'License: Apache 2.0 - https://github.com/psf/requests/blob/main/LICENSE\n'
    '---\n'
    'python-sounddevice - https://github.com/spatialaudio/python-sounddevice\n'
    'License: MIT - https://github.com/spatialaudio/python-sounddevice/blob/master/LICENSE'
)

CONFIG_DEFAULTS = {
    'connection-timeout': 5.0,
    'volume': 1.0
}

USER_AGENT = f'Eternal Radio Player/{__version__}'

STREAM_URL = 'https://radio.jump.bg/proxy/mnikolov/stream'
STREAM_ITER_CHUNK_SIZE = 16 * 1024

PLAYER_FRAME_COUNT = 4 * 1024

RECENT_SONGS_URL = 'https://radio.jump.bg/recentfeed/mnikolov/json'
RECENT_SONGS_CACHE_TIME = 10.0
