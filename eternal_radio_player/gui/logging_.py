import logging
from PySide6 import QtCore


class _SignalProxy(QtCore.QObject):

    message = QtCore.Signal(str)


class QPlainTextEditHandler(logging.Handler):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = widget
        self._signal_proxy = _SignalProxy()
        self.message = self._signal_proxy.message

    def emit(self, record):
        self._signal_proxy.message.emit(self.format(record))
