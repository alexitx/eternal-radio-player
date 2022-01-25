import json
import logging
import time
import miniaudio
import numpy
import requests
import requests.exceptions
import sounddevice
from threading import Lock

from .constants import (
    PLAYER_FRAME_COUNT,
    RECENT_SONGS_CACHE_TIME,
    RECENT_SONGS_URL,
    REQUEST_TIMEOUT
)
from .exceptions import PlayerError
from .stream import HTTPStreamSource, stream_request


log = logging.getLogger(__name__)


class RadioPlayer:

    recent_songs_cache_time = RECENT_SONGS_CACHE_TIME
    _recent_songs_cache_last = 0.0
    _recent_songs_cache_data = None

    def __init__(self, request_timeout=REQUEST_TIMEOUT):
        self.running = False
        self.request_timeout = request_timeout
        self._stream_source = None
        self._input_stream = None
        self._output_stream = None
        self._linear_volume = 1.0
        self._volume = 1.0
        self._lock = Lock()

    def play(self):
        if self.running:
            log.debug('Cannot start radio player, already running')
            return
        with self._lock:
            log.debug('Starting radio player')
            self._stop_output()
            self._stop_input()
            try:
                self._init()
            except Exception as e:
                raise PlayerError(f'Could not initialize player: {e}') from e
            self._output_stream.start()
            self.running = True

    def stop(self):
        with self._lock:
            log.debug('Stopping radio player')
            self._stop_output()
            self._stop_input()
            self.running = False

    def get_volume(self):
        return self._linear_volume

    def set_volume(self, volume):
        self._linear_volume = volume
        self._volume = volume ** 3

    @classmethod
    def get_recent_songs(cls, url=RECENT_SONGS_URL, timeout=REQUEST_TIMEOUT):
        if time.time() - cls._recent_songs_cache_last <= cls.recent_songs_cache_time:
            return cls._recent_songs_cache_data
        try:
            response = requests.get(url=url, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise PlayerError(f'Could not fetch recent songs: {e}') from e
        try:
            items = response.json()['items']
            recent_songs = []
            for recent_song in items:
                title = recent_song['title'][:-6].strip() # Remove ID '[XXXX]' at the end
                timestamp = min(int(recent_song['date']), int(time.time()))
                recent_songs.append({'title': title, 'timestamp': timestamp})
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise PlayerError('Received bad recent songs data') from e
        cls._recent_songs_cache_data = recent_songs
        cls._recent_songs_cache_last = time.time()
        return recent_songs

    def _init(self):
        request, encoding, sample_rate = stream_request(timeout=self.request_timeout)
        if not sample_rate:
            sample_rate = sounddevice.default.samplerate or 44100
        log.debug(
            f'Initializing player with request status: {request.status_code}, '
            f'encoding: {encoding}, sample rate: {sample_rate}'
        )
        self._output_stream = sounddevice.OutputStream(
            samplerate=sample_rate,
            blocksize=PLAYER_FRAME_COUNT,
            channels=2,
            dtype=numpy.float32,
            callback=self._stream_callback_wrapper,
            finished_callback=self._finished_callback
        )
        self._stream_source = HTTPStreamSource(request)
        self._input_stream = miniaudio.stream_any(
            source=self._stream_source,
            source_format=encoding,
            output_format=miniaudio.SampleFormat.FLOAT32,
            nchannels=2,
            sample_rate=sample_rate,
            frames_to_read=PLAYER_FRAME_COUNT,
            dither=miniaudio.DitherMode.TRIANGLE
        )

    def _stream_callback_wrapper(self, *args, **kwargs):
        try:
            self._stream_callback(*args, **kwargs)
            return
        except sounddevice.CallbackAbort:
            raise
        except miniaudio.MiniaudioError as e:
            log.error(f'Decoder error: {e}')
        except Exception as e:
            log.error(f'Stream callback exception: {e}')
        raise sounddevice.CallbackAbort

    def _stream_callback(self, output, frames, _time, status):
        if status and status.output_underflow:
            log.warning('Output buffer underflow')
        raw_samples = self._input_stream.send(frames)
        samples = numpy.asarray(raw_samples, raw_samples.typecode).reshape(-1, 2) * self._volume
        if len(samples) < len(output):
            log.error(f'Length of stream data is less than expected: ({len(samples)}/{len(output)})')
            raise sounddevice.CallbackAbort
        output[:] = samples

    def _finished_callback(self):
        log.debug('Stream callback stopped')
        if self._lock.acquire(False):
            self._stop_input()
            self.running = False
            self._lock.release()

    def _stop_input(self):
        if self._input_stream:
            log.debug('Closing and destroying input stream')
            self._input_stream.close()
            self._input_stream = None

    def _stop_output(self):
        if self._output_stream:
            log.debug('Closing and destroying output stream')
            self._output_stream.abort()
            self._output_stream.close()
            self._output_stream = None
