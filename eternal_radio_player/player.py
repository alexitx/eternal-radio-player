import logging
import miniaudio
import numpy
import sounddevice
from threading import Lock

from .constants import PLAYER_FRAME_COUNT
from .exceptions import PlayerError
from .stream import HTTPStreamSource, stream_request


log = logging.getLogger(__name__)


class RadioPlayer:

    def __init__(self):
        self.running = False
        self._input_stream = None
        self._output_stream = None
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

    def set_volume(self, volume):
        self._volume = volume ** 3

    def _init(self):
        request, encoding, sample_rate = stream_request()
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
        self._input_stream = miniaudio.stream_any(
            source=HTTPStreamSource(request),
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
