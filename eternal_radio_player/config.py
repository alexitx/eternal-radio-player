import errno
import json
import logging
import os.path
import platform
import platformdirs
import schema
from pathlib import Path

from .constants import CONFIG_DEFAULTS
from .exceptions import ConfigError


log = logging.getLogger(__name__)


class Config:

    data = {}
    _file = None
    _schema = schema.Schema(
        {
            schema.Optional('connection-timeout'): float,
            schema.Optional('volume'): float
        },
        ignore_extra_keys=True
    )

    @classmethod
    def init(cls, file=None):
        log.info('Initializing configuration')

        if file:
            config_dir = Path(os.path.dirname(file))
            config_file = Path(file)
        else:
            if platform.system() == 'Windows':
                dir_name = 'Eternal Radio Player'
            else:
                dir_name = 'eternal-radio-player'
            config_dir = platformdirs.user_config_path(dir_name, False)
            config_file = config_dir.joinpath('config.json')
            log.debug(f"Creating configuration directory: '{config_dir}'")

        try:
            config_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ConfigError(f'Could not create config directory: {e}') from e

        log.debug(f'Configuration file: {config_file}')
        cls._file = str(config_file)

    @classmethod
    def load(cls, defaults=None):
        if not defaults:
            defaults = {}

        log.info('Loading configuration')

        # Load the config file if it exists, else use empty dict
        try:
            with open(cls._file, 'r', encoding='utf-8') as f:
                raw_config_data = json.load(f)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise ConfigError(f'Could not load config: {e}') from e
            raw_config_data = {}
        except json.JSONDecodeError as e:
            raise ConfigError(f'Could not load config: {e}') from e

        # Validate the loaded config and update missing values with defaults
        try:
            cls._schema.validate(raw_config_data)
        except schema.SchemaError as e:
            raise ConfigError(f'Could not load config: {e}') from e

        config_data = CONFIG_DEFAULTS.copy()
        config_data.update({**defaults, **raw_config_data})
        cls.data = config_data

    @classmethod
    def save(cls, defaults=None, write_defaults=False):
        if not defaults:
            defaults = {}

        log.info('Saving configuration')

        try:
            with open(cls._file, 'w', encoding='utf-8') as f:
                if write_defaults:
                    config_data = CONFIG_DEFAULTS.copy()
                    config_data.update(defaults)
                    json.dump(config_data, f)
                else:
                    json.dump(cls.data, f)
        except (OSError, json.JSONDecodeError) as e:
            raise ConfigError(f'Could not save config: {e}') from e
