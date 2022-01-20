import logging
import miniaudio
import requests

from .constants import REQUEST_TIMEOUT, STREAM_ITER_CHUNK_SIZE, STREAM_URL, USER_AGENT
from .exceptions import StreamError


log = logging.getLogger(__name__)


class HTTPStreamSource(miniaudio.StreamableSource):

    def __init__(self, request, iter_chunk_size=STREAM_ITER_CHUNK_SIZE):
        super().__init__()
        self._request = request
        self._stream_iter = self._request.raw.stream(iter_chunk_size, False)
        self._buffer = bytearray()

    def read(self, size):
        if self._request.raw.closed:
            raise StreamError('Cannot read from a closed stream')
        while len(self._buffer) < size:
            try:
                self._buffer.extend(next(self._stream_iter))
            except StopIteration:
                break
        data = self._buffer[:size]
        del self._buffer[:size]
        return data


def stream_request(url=STREAM_URL, user_agent=USER_AGENT, timeout=REQUEST_TIMEOUT, **kwargs):
    log.debug(f"Making stream request with URL: '{url}', timeout: {timeout}")

    response = requests.get(
        url=url,
        headers={'User-Agent': user_agent},
        timeout=timeout,
        stream=True,
        **kwargs
    )

    content_type = response.headers.get('Content-Type')
    if content_type == 'audio/mpeg':
        encoding = miniaudio.FileFormat.MP3
    elif content_type == 'audio/ogg':
        encoding = miniaudio.FileFormat.VORBIS
    else:
        raise ValueError(f'Unsupported stream encoding: {content_type}')

    icy_sr = response.headers.get('icy-sr')
    try:
        sample_rate = int(icy_sr)
    except ValueError:
        sample_rate = None

    return response, encoding, sample_rate
