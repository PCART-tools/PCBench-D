class HttpMessage:
    """HttpMessage allows to write headers and payload to a stream.

    For example, lets say we want to read file then compress it with deflate
    compression and then send it with chunked transfer encoding, code may look
    like this:

       >> response = aiohttp.Response(transport, 200)

    We have to use deflate compression first:

      >> response.add_compression_filter('deflate')

    Then we want to split output stream into chunks of 1024 bytes size:

      >> response.add_chunking_filter(1024)

    We can add headers to response with add_headers() method. add_headers()
    does not send data to transport, send_headers() sends request/response
    line and then sends headers:

      >> response.add_headers(
      ..     ('Content-Disposition', 'attachment; filename="..."'))
      >> response.send_headers()

    Now we can use chunked writer to write stream to a network stream.
    First call to write() method sends response status line and headers,
    add_header() and add_headers() method unavailble at this stage:

    >> with open('...', 'rb') as f:
    ..     chunk = fp.read(8196)
    ..     while chunk:
    ..         response.write(chunk)
    ..         chunk = fp.read(8196)

    >> response.write_eof()
    """

    writer = None

    # 'filter' is being used for altering write() bahaviour,
    # add_chunking_filter adds deflate/gzip compression and
    # add_compression_filter splits incoming data into a chunks.
    filter = None

    HOP_HEADERS = None  # Must be set by subclass.

    SERVER_SOFTWARE = 'Python/{0[0]}.{0[1]} aiohttp/{1}'.format(
        sys.version_info, aiohttp.__version__)

    status = None
    status_line = b''
    upgrade = False  # Connection: UPGRADE
    websocket = False  # Upgrade: WEBSOCKET

    # subclass can enable auto sending headers with write() call,
    # this is useful for wsgi's start_response implementation.
    _send_headers = False

    _has_user_agent = False

    def __init__(self, transport, version, close):
        self.transport = transport
        self.version = version
        self.closing = close

        # disable keep-alive for http/1.0
        if version <= (1, 0):
            self.keepalive = False
        else:
            self.keepalive = None

        self.chunked = False
        self.length = None
        self.headers = multidict.CaseInsensitiveMutableMultiDict()
        self.headers_sent = False
        self.output_length = 0
        self._output_size = 0

    def force_close(self):
        self.closing = True
        self.keepalive = False

    def force_chunked(self):
        self.chunked = True

    def keep_alive(self):
        if self.keepalive is None:
            return not self.closing
        else:
            return self.keepalive

    def is_headers_sent(self):
        return self.headers_sent

    def add_header(self, name, value):
        """Analyze headers. Calculate content length,
        removes hop headers, etc."""
        assert not self.headers_sent, 'headers have been sent already'
        assert isinstance(name, str), '{!r} is not a string'.format(name)
        assert isinstance(value, str), '{!r} is not a string'.format(value)

        name = name.strip().upper()
        value = value.strip()

        if name == 'CONTENT-LENGTH':
            self.length = int(value)

        if name == 'CONNECTION':
            val = value.lower()
            # handle websocket
            if 'upgrade' in val:
                self.upgrade = True
            # connection keep-alive
            elif 'close' in val:
                self.keepalive = False
            elif 'keep-alive' in val and self.version >= (1, 1):
                self.keepalive = True

        elif name == 'UPGRADE':
            if 'websocket' in value.lower():
                self.websocket = True
                self.headers[name] = value

        elif name == 'TRANSFER-ENCODING' and not self.chunked:
            self.chunked = value.lower().strip() == 'chunked'

        elif name not in self.HOP_HEADERS:
            if name == 'USER-AGENT':
                self._has_user_agent = True

            # ignore hopbyhop headers
            self.headers.add(name, value)

    def add_headers(self, *headers):
        """Adds headers to a http message."""
        for name, value in headers:
            self.add_header(name, value)

    def send_headers(self):
        """Writes headers to a stream. Constructs payload writer."""
        # Chunked response is only for HTTP/1.1 clients or newer
        # and there is no Content-Length header is set.
        # Do not use chunked responses when the response is guaranteed to
        # not have a response body (304, 204).
        assert not self.headers_sent, 'headers have been sent already'
        self.headers_sent = True

        if (self.chunked is True) or (
                self.length is None and
                self.version >= (1, 1) and
                self.status not in (304, 204)):
            self.chunked = True
            self.writer = self._write_chunked_payload()

        elif self.length is not None:
            self.writer = self._write_length_payload(self.length)

        else:
            self.writer = self._write_eof_payload()

        next(self.writer)

        self._add_default_headers()

        # status + headers
        hdrs = ''.join(itertools.chain(
            (self.status_line,),
            *((k, ': ', v, '\r\n')
              for k, v in ((k, value)
                           for k, value in self.headers.items(getall=True)))))
        hdrs = hdrs.encode('utf-8') + b'\r\n'

        self.output_length += len(hdrs)
        self.transport.write(hdrs)

    def _add_default_headers(self):
        # set the connection header
        if self.upgrade:
            connection = 'upgrade'
        elif not self.closing if self.keepalive is None else self.keepalive:
            connection = 'keep-alive'
        else:
            connection = 'close'

        if self.chunked:
            self.headers['TRANSFER-ENCODING'] = 'chunked'

        self.headers['CONNECTION'] = connection

    def write(self, chunk):
        """write() writes chunk of data to a steram by using different writers.
        writer uses filter to modify chunk of data. write_eof() indicates
        end of stream. writer can't be used after write_eof() method
        being called. write() return drain future.
        """
        assert (isinstance(chunk, (bytes, bytearray)) or
                chunk is EOF_MARKER), chunk

        size = self.output_length

        if self._send_headers and not self.headers_sent:
            self.send_headers()

        assert self.writer is not None, 'send_headers() is not called.'

        if self.filter:
            chunk = self.filter.send(chunk)
            while chunk not in (EOF_MARKER, EOL_MARKER):
                self.writer.send(chunk)
                chunk = next(self.filter)
        else:
            if chunk is not EOF_MARKER:
                self.writer.send(chunk)

        self._output_size += self.output_length - size

        if self._output_size > 64 * 1024:
            self._output_size = 0
            return self.transport.drain()
        else:
            return ()

    def write_eof(self):
        self.write(EOF_MARKER)
        try:
            self.writer.throw(aiohttp.EofStream())
        except StopIteration:
            pass

        return self.transport.drain()

    def _write_chunked_payload(self):
        """Write data in chunked transfer encoding."""
        while True:
            try:
                chunk = yield
            except aiohttp.EofStream:
                self.transport.write(b'0\r\n\r\n')
                self.output_length += 5
                break

            chunk = bytes(chunk)
            chunk_len = '{:x}\r\n'.format(len(chunk)).encode('ascii')
            self.transport.write(chunk_len)
            self.transport.write(chunk)
            self.transport.write(b'\r\n')
            self.output_length += len(chunk_len) + len(chunk) + 2

    def _write_length_payload(self, length):
        """Write specified number of bytes to a stream."""
        while True:
            try:
                chunk = yield
            except aiohttp.EofStream:
                break

            if length:
                l = len(chunk)
                if length >= l:
                    self.transport.write(chunk)
                    self.output_length += len(chunk)
                else:
                    self.transport.write(chunk[:length])
                    self.output_length += length

                length = max(0, length-l)

    def _write_eof_payload(self):
        while True:
            try:
                chunk = yield
            except aiohttp.EofStream:
                break

            self.transport.write(chunk)
            self.output_length += len(chunk)

    @wrap_payload_filter
    def add_chunking_filter(self, chunk_size=16*1024):
        """Split incoming stream into chunks."""
        buf = bytearray()
        chunk = yield

        while True:
            if chunk is EOF_MARKER:
                if buf:
                    yield buf

                yield EOF_MARKER

            else:
                buf.extend(chunk)

                while len(buf) >= chunk_size:
                    chunk = bytes(buf[:chunk_size])
                    del buf[:chunk_size]
                    yield chunk

                chunk = yield EOL_MARKER

    @wrap_payload_filter
    def add_compression_filter(self, encoding='deflate'):
        """Compress incoming stream with deflate or gzip encoding."""
        zlib_mode = (16 + zlib.MAX_WBITS
                     if encoding == 'gzip' else -zlib.MAX_WBITS)
        zcomp = zlib.compressobj(wbits=zlib_mode)

        chunk = yield
        while True:
            if chunk is EOF_MARKER:
                yield zcomp.flush()
                chunk = yield EOF_MARKER

            else:
                yield zcomp.compress(chunk)
                chunk = yield EOL_MARKER
