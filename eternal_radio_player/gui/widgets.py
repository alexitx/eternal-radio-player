from PySide6 import QtCore, QtGui, QtWidgets


class ControlToolButton(QtWidgets.QToolButton):

    hovered = QtCore.Signal(bool)
    focused = QtCore.Signal(bool)

    def enterEvent(self, event):
        self.hovered.emit(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered.emit(False)
        super().leaveEvent(event)

    def focusInEvent(self, event):
        self.focused.emit(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.focused.emit(False)
        super().focusOutEvent(event)


class RecentSong(QtWidgets.QWidget):

    def __init__(
        self,
        parent=None,
        title=None,
        timestamp=None,
        margins=8,
        spacing=6,
        title_font_size=12,
        timestamp_font_size=10,
        **kwargs
    ):
        super().__init__(parent=parent, **kwargs)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(margins, margins, margins, margins)
        self._layout.setSpacing(spacing)
        self.title = QtWidgets.QLabel(self, text=title)
        self.title.setObjectName('title')
        self.title.setWordWrap(True)
        self.set_title_font_size(title_font_size)
        self.timestamp = QtWidgets.QLabel(self, text=timestamp)
        self.timestamp.setObjectName('timestamp')
        self.timestamp.setWordWrap(True)
        self.set_timestamp_font_size(timestamp_font_size)
        self._layout.addWidget(self.title)
        self._layout.addWidget(self.timestamp)
        self.setLayout(self._layout)

    def set_title_font_size(self, value):
        font = self.title.font()
        font.setPointSize(value)
        self.title.setFont(font)

    def set_timestamp_font_size(self, value):
        font = self.timestamp.font()
        font.setPointSize(value)
        self.timestamp.setFont(font)

    def paintEvent(self, pe):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        s = self.style()
        s.drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)
