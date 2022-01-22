import argparse
import cmd
import logging
import os.path
import platform
import sys
import platformdirs
import timeago
from pathlib import Path

from ._version import __version__
from .config import Config
from .constants import CREDITS
from .exceptions import PlayerError
from .player import RadioPlayer
from .utils import format_exc, system_info


log = logging.getLogger(__name__)


class App(cmd.Cmd):

    prompt = '> '
    intro = (
        f"\nEternal Radio Player {__version__}\n"
        "Type 'help' for a list of commands or 'quit' to exit\n"
    )
    _hidden_attrs = ('do_EOF', 'do_help')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.debug('Initializing CLI command logger')
        logger = logging.getLogger('cli-cmd')
        logger.propagate = False
        logger.setLevel(logging.NOTSET)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        self._log = logger
        self._player = RadioPlayer()
        self._player.set_volume(Config.data['volume'])

    def do_play(self, _):
        try:
            self._player.play()
        except PlayerError as e:
            log.error(f'Error starting player: {e}')

    def do_stop(self, _):
        self._player.stop()

    def do_volume(self, args):
        if not args:
            self._log.info('Not enough arguments')
            return
        try:
            volume = int(args)
        except ValueError:
            self._log.info(f"Invalid value '{args}'")
            return
        if not 0 <= volume <= 100:
            self._log.info('The value must be within range 0-100')
            return
        volume_float = volume / 100
        self._player.set_volume(volume_float)
        Config.data['volume'] = volume_float

    def do_recent(self, _):
        recent_songs_localized = []
        for recent_song in self._player.get_recent_songs():
            title = recent_song['title']
            timestamp = recent_song['timestamp']
            timestamp_fmt = timeago.format(timestamp)
            recent_songs_localized.append(f'{title}\n{timestamp_fmt}')
        self._log.info('\n\n'.join(recent_songs_localized))

    def do_config(self, args):
        if not args:
            self._log.info('Not enough arguments')
            return

        args = args.split(' ', 1)
        subcmd = args[0]
        value = args[1] if len(args) > 1 else None

        if subcmd == 'connection-timeout':
            if value is None:
                connection_timeout = Config.data['connection-timeout']
                self._log.info(f"Connection Timeout: {connection_timeout}s")
                return

            try:
                connection_timeout = float(value)
            except ValueError:
                self._log.info(f"Invalid value '{value}'")
                return
            if not 1.0 <= connection_timeout <= 60.0:
                self._log.info('The value be within range 1-60')
                return

            self._log.info(f'Connection Timeout: {connection_timeout}s')
            Config.data['connection-timeout'] = connection_timeout
        elif subcmd == 'save':
            Config.save()
        else:
            self._log.info(f"Invalid argument '{subcmd}'")

    def do_about(self, _):
        self._log.info(f'{system_info()}\n\n{CREDITS}')

    def do_quit(self, _):
        self._player.stop()
        Config.save()
        return True

    def do_help(self, args):
        if args:
            print()
        super().do_help(args)
        if args:
            print()

    def help_play(self):
        self._log.info(
            'Start the radio player\n\n'
            'Usage:\n'
            '  play'
        )

    def help_stop(self):
        self._log.info(
            'Stop the radio player\n\n'
            'Usage:\n'
            '  stop'
        )

    def help_volume(self):
        self._log.info(
            'View or change the sound volume\n\n'
            'Usage:\n'
            '  volume [0-100]'
        )

    def help_recent(self):
        self._log.info(
            'View the recently played songs\n\n'
            'Usage:\n'
            '  recent'
        )

    def help_config(self):
        self._log.info(
            'View or change the configuration\n\n'
            'Usage:\n'
            '  config connection-timeout [value]\n'
            '  config save'
        )

    def help_about(self):
        self._log.info(
            'View information about this app and the system\n\n'
            'Usage:\n'
            '  about'
        )

    def help_quit(self):
        self._log.info(
            'Quit the application\n\n'
            'Usage:\n'
            '  quit'
        )

    def get_names(self):
        return [n for n in dir(self.__class__) if n not in self._hidden_attrs]

    def cmdloop(self, *args, **kwargs) -> None:
        try:
            super().cmdloop(*args, **kwargs)
        except KeyboardInterrupt:
            log.debug('Received KeyboardInterrupt, stopping and exiting')
            self._player.stop()
            raise


def main():

    class HelpFormatter(argparse.HelpFormatter):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, max_help_position=32, **kwargs)

        def _format_action_invocation(self, action):
            if not action.option_strings or action.nargs == 0:
                return super()._format_action_invocation(action)
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            return f"{', '.join(action.option_strings)} {args_string}"

    parser = argparse.ArgumentParser(formatter_class=HelpFormatter)
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'Eternal Radio Player {__version__}'
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Set logging verbosity to debug'
    )
    parser.add_argument(
        '-l',
        '--log',
        help='Log file path',
        metavar='<file>'
    )
    parser.add_argument(
        '-c',
        '--config',
        help='Config file path',
        metavar='<file>'
    )
    args = parser.parse_args()

    def error(msg, exc=None, tb=False):
        if exc:
            print(f'{msg}: {format_exc(exc, tb)}', file=sys.stderr)
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    if args.log:
        log_dir = Path(os.path.dirname(args.log))
        log_file = Path(args.log)
    else:
        if platform.system() == 'Windows':
            dir_name = 'Eternal Radio Player'
        else:
            dir_name = 'eternal-radio-player'
        log_dir = platformdirs.user_log_path(dir_name, False)
        log_file = log_dir.joinpath('eternal-radio-player.log')
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        error(f"Could not create log directory '{log_dir}'", e)

    root_logger = logging.getLogger()
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s:%(funcName)s]: %(message)s')
    stream_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(logging.NOTSET if args.debug else logging.INFO)
    file_handler = logging.FileHandler(str(log_file), 'w', 'utf-8')
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.NOTSET)

    log.debug(f'System information:\n{system_info()}')

    Config.init(args.config)
    Config.load()

    try:
        App().cmdloop()
        log.info('Exiting')
        sys.exit()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(1)
