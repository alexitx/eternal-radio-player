class EternalRadioPlayerError(Exception):
    pass


class ConfigError(EternalRadioPlayerError):
    pass


class StreamError(EternalRadioPlayerError):
    pass


class PlayerError(EternalRadioPlayerError):
    pass


class ResourceError(EternalRadioPlayerError):
    pass


class I18nError(EternalRadioPlayerError):
    pass
