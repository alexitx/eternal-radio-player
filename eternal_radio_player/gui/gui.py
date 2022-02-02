import logging
import time
import timeago
import qdarktheme
from functools import partial
from PySide6 import QtCore, QtGui, QtWidgets

from ..config import Config
from ..constants import CREDITS, RECENT_SONGS_UPDATE_TIME, REQUEST_TIMEOUT
from ..exceptions import PlayerError
from ..player import RadioPlayer
from ..utils import qt_resource, system_info
from .generated.main_window import Ui_MainWindow
from .logging_ import QPlainTextEditHandler
from .widgets import RecentSong


log = logging.getLogger(__name__)


class RecentSongsUpdateWorker(QtCore.QObject):

    result = QtCore.Signal(list)

    def __init__(self, update_time=RECENT_SONGS_UPDATE_TIME, timeout=REQUEST_TIMEOUT, **kwargs):
        super().__init__(**kwargs)
        self.update_time = update_time
        self.timeout = timeout
        self._running = False

    def run(self):
        self._running = True
        try:
            data = RadioPlayer.get_recent_songs(self.timeout)
        except PlayerError as e:
            log.error(f'Recent songs update worker error: {e}')
        else:
            self.result.emit(data)
        last_update = time.time()
        while self._running:
            if time.time() - last_update < self.update_time:
                time.sleep(1)
                continue
            try:
                data = RadioPlayer.get_recent_songs(self.timeout)
            except PlayerError as e:
                log.error(f'Recent songs update worker error: {e}')
            else:
                self.result.emit(data)
            last_update = time.time()

    def stop(self):
        self._running = False


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, logging_level=logging.INFO, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set up logging handler for the console
        log.debug('Initializing GUI console logging handler')
        root_logger = logging.getLogger()
        self.console_handler = QPlainTextEditHandler(self.ui.console, level=logging_level)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%H:%M:%S')
        self.console_handler.setFormatter(formatter)
        self.console_handler.message.connect(self.ui.console.appendPlainText)
        root_logger.addHandler(self.console_handler)

        self.player = RadioPlayer()
        self.player.set_volume(Config.data['volume'])
        self.playing = False
        self.muted = False

        self.play_icon_normal = QtGui.QIcon(':icons/play.svg')
        self.play_icon_accent = QtGui.QIcon(':icons/play_accent.svg')
        self.stop_icon_normal = QtGui.QIcon(':icons/stop.svg')
        self.stop_icon_accent = QtGui.QIcon(':icons/stop_accent.svg')
        self.volume_normal_icon_normal = QtGui.QIcon(':icons/volume-normal.svg')
        self.volume_normal_icon_accent = QtGui.QIcon(':icons/volume-normal_accent.svg')
        self.volume_muted_icon_normal = QtGui.QIcon(':icons/volume-muted.svg')
        self.volume_muted_icon_accent = QtGui.QIcon(':icons/volume-muted_accent.svg')
        self.output_device_icon_normal = QtGui.QIcon(':icons/output-device.svg')
        self.output_device_icon_accent = QtGui.QIcon(':icons/output-device_accent.svg')
        self.console_icon_normal = QtGui.QIcon(':icons/console.svg')
        self.console_icon_accent = QtGui.QIcon(':icons/console_accent.svg')
        self.settings_icon_normal = QtGui.QIcon(':icons/settings.svg')
        self.settings_icon_accent = QtGui.QIcon(':icons/settings_accent.svg')

        # Assign generic handlers for control button events
        control_buttons_icons = (
            (self.ui.output_device_button, self.output_device_icon_normal, self.output_device_icon_accent),
            (self.ui.console_button, self.console_icon_normal, self.console_icon_accent),
            (self.ui.settings_button, self.settings_icon_normal, self.settings_icon_accent)
        )
        for widget, icon_normal, icon_accent in control_buttons_icons:
            fn = partial(self.set_widget_icon, widget, icon_normal, icon_accent)
            widget.hovered.connect(fn)
            widget.focused.connect(fn)

        # Assign special handlers for play/stop and mute/unmute button events
        self.ui.play_button.hovered.connect(self.set_play_button_icon)
        self.ui.play_button.focused.connect(self.set_play_button_icon)
        self.ui.play_button.toggled.connect(self.on_play)
        self.ui.volume_button.hovered.connect(self.set_volume_button_icon)
        self.ui.volume_button.focused.connect(self.set_volume_button_icon)
        self.ui.volume_button.clicked.connect(self.on_mute)

        self.ui.volume_slider.setValue(int(Config.data['volume'] * 100))
        self.ui.volume_slider.valueChanged.connect(self.on_volume_change)

        self.ui.console_button.clicked.connect(lambda: self.ui.main_widget.setCurrentIndex(1))
        self.ui.settings_button.clicked.connect(lambda: self.ui.main_widget.setCurrentIndex(2))

        # Setup console page widgets
        console_font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
        console_font.setPointSize(8)
        self.ui.console.setFont(console_font)
        self.ui.console_back_button.clicked.connect(lambda: self.ui.main_widget.setCurrentIndex(0))

        # Setup settings page widgets
        settings_infos_font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
        settings_infos_font.setPointSize(9)
        self.ui.system_info.setFont(settings_infos_font)
        self.ui.credits.setFont(settings_infos_font)
        self.ui.system_info.setPlainText(system_info())
        self.ui.credits.setPlainText(CREDITS)
        self.ui.connection_timeout_input.setValue(Config.data['connection-timeout'])
        self.ui.recent_songs_update_time_input.setValue(Config.data['recent-songs-update-time'])
        self.ui.settings_save_button.clicked.connect(self.save_settings)
        self.ui.settings_back_button.clicked.connect(lambda: self.ui.main_widget.setCurrentIndex(0))

        # Setup recent songs page widgets
        self.recent_songs_container_layout = QtWidgets.QVBoxLayout(self.ui.recent_songs_container)
        self.recent_songs_container_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_songs_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        # Setup recent songs update worker
        self.recent_songs_widgets = []
        self.recent_songs_update_worker_thread = QtCore.QThread(self)
        self.recent_songs_update_worker = RecentSongsUpdateWorker(Config.data['recent-songs-update-time'])
        self.recent_songs_update_worker.result.connect(self.update_recent_songs)
        self.recent_songs_update_worker.moveToThread(self.recent_songs_update_worker_thread)
        self.recent_songs_update_worker_thread.started.connect(self.recent_songs_update_worker.run)

        log.info('GUI initialized')

        log.debug('Starting recent songs update worker')
        self.recent_songs_update_worker_thread.start()

    def on_play(self, state):
        self.playing = state
        self.set_play_button_icon(self.ui.play_button.underMouse() or self.ui.play_button.hasFocus())
        self.ui.play_button.repaint()
        if self.playing:
            try:
                self.player.play()
            except PlayerError as e:
                log.error(f'Could not start player: {e}')
                self.ui.play_button.setChecked(False)
                return
            self.ui.play_button.setToolTip('Stop')
        else:
            self.player.stop()
            self.ui.play_button.setToolTip('Play')

    def on_mute(self, state):
        self.muted = state
        self.set_volume_button_icon(self.ui.volume_button.underMouse() or self.ui.volume_button.hasFocus())
        if self.muted:
            self.player.set_volume(0.0)
            self.ui.volume_button.setToolTip('Unmute')
        else:
            self.player.set_volume(self.ui.volume_slider.value() / 100)
            self.ui.volume_button.setToolTip('Mute')

    def on_volume_change(self, value):
        volume = value / 100
        if not self.muted:
            self.player.set_volume(volume)
        Config.data['volume'] = volume

    def set_widget_icon(self, widget, icon_normal, icon_accent=None, highlight=False):
        if highlight and icon_accent:
            widget.setIcon(icon_accent)
        else:
            widget.setIcon(icon_normal)

    def set_play_button_icon(self, highlight):
        if self.playing:
            self.set_widget_icon(self.ui.play_button, self.stop_icon_normal, self.stop_icon_accent, highlight)
        else:
            self.set_widget_icon(self.ui.play_button, self.play_icon_normal, self.play_icon_accent, highlight)

    def set_volume_button_icon(self, highlight):
        if self.muted:
            self.set_widget_icon(
                self.ui.volume_button,
                self.volume_muted_icon_normal,
                self.volume_muted_icon_accent,
                highlight
            )
        else:
            self.set_widget_icon(
                self.ui.volume_button,
                self.volume_normal_icon_normal,
                self.volume_normal_icon_accent,
                highlight
            )

    def save_settings(self):
        connection_timeout = self.ui.connection_timeout_input.value()
        self.recent_songs_update_worker.timeout = connection_timeout
        Config.data['connection-timeout'] = connection_timeout
        recent_songs_update_time = self.ui.recent_songs_update_time_input.value()
        self.recent_songs_update_worker.update_time = recent_songs_update_time
        Config.data['recent-songs-update-time'] = recent_songs_update_time
        Config.save()

    def update_recent_songs(self, recent_songs):
        for recent_song_widget in self.recent_songs_widgets:
            recent_song_widget.deleteLater()
        self.recent_songs_widgets.clear()
        self.recent_songs_container_layout.removeItem(self.recent_songs_spacer)

        for i, recent_song in enumerate(recent_songs):
            title = recent_song['title']
            timestamp = recent_song['timestamp']
            timestamp_fmt = timeago.format(timestamp)

            recent_song = RecentSong(self.ui.recent_songs_container, title, timestamp_fmt)
            recent_song.setObjectName('recent_song_entry')
            if i % 2 == 0:
                recent_song.setProperty('class', 'alternate')

            self.recent_songs_container_layout.addWidget(recent_song)
            self.recent_songs_widgets.append(recent_song)
        self.recent_songs_container_layout.addSpacerItem(self.recent_songs_spacer)

    def closeEvent(self, event):
        log.debug('Stopping recent songs update worker')
        self.recent_songs_update_worker.stop()
        self.recent_songs_update_worker_thread.quit()
        self.recent_songs_update_worker_thread.wait()
        self.recent_songs_update_worker.deleteLater()
        Config.save()
        super().closeEvent(event)


def gui_main():
    # Enable high DPI support
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication()

    # Set global font size
    font = app.font()
    font.setPointSize(11)
    app.setFont(font)

    # Load and apply stylesheets
    custom_stylesheet = qt_resource(':style.qss')
    qdarktheme_stylesheet = qdarktheme.load_stylesheet('dark')
    app.setStyleSheet(qdarktheme_stylesheet + custom_stylesheet)

    main_window = MainWindow()
    main_window.show()
    return app.exec()
