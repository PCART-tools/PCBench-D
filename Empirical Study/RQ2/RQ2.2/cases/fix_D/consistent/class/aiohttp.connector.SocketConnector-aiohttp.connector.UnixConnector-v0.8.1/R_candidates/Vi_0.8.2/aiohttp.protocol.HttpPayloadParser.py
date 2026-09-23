class HttpPayloadParser:

    def __init__(self, message, length=None, compression=True, readall=False):
        self.message = message
        self.length = length
        self.compression = compression
        self.readall = readall

    def __call__(self, out, buf):
        # payload params
        length = self.message.headers.get('CONTENT-LENGTH', self.length)
        if 'SEC-WEBSOCKET-KEY1' in self.message.headers:
            length = 8

        # payload decompression wrapper
        if self.compression and self.message.compression:
            out = DeflateBuffer(out, self.message.compression)

        # payload parser
        if 'chunked' in self.message.headers.get('TRANSFER-ENCODING', ''):
            yield from self.parse_chunked_payload(out, buf)

        elif length is not None:
            try:
                length = int(length)
            except ValueError:
                raise errors.InvalidHeader('CONTENT-LENGTH') from None

            if length < 0:
                raise errors.InvalidHeader('CONTENT-LENGTH')
            elif length > 0:
                yield from self.parse_length_payload(out, buf, length)
        else:
            if self.readall and getattr(self.message, 'code', 0) != 204:
                yield from self.parse_eof_payload(out, buf)
            elif getattr(self.message, 'method', None) in ('PUT', 'POST'):
                logging.warn(  # pragma: no cover
                    'Content-Length or Transfer-Encoding header is required')

        out.feed_eof()

    def parse_chunked_payload(self, out, buf):
        """Chunked transfer encoding parser."""
        try:
            while True:
                # read next chunk size
                line = yield from buf.readuntil(b'\r\n', 8196)

                i = line.find(b';')
                if i >= 0:
                    line = line[:i]  # strip chunk-extensions
                else:
                    line = line.strip()
                try:
                    size = int(line, 16)
                except ValueError:
                    raise errors.IncompleteRead(b'') from None

                if size == 0:  # eof marker
                    break

                # read chunk and feed buffer
                while size:
                    chunk = yield from buf.readsome(size)
                    out.feed_data(chunk)
                    size = size - len(chunk)

                # toss the CRLF at the end of the chunk
                yield from buf.skip(2)

            # read and discard trailer up to the CRLF terminator
            yield from buf.skipuntil(b'\r\n')

        except aiohttp.EofStream:
            raise errors.ConnectionError('Broken chunked payload.') from None

    def parse_length_payload(self, out, buf, length=0):
        """Read specified amount of bytes."""
        required = length
        try:
            while required:
                chunk = yield from buf.readsome(required)
                out.feed_data(chunk)
                required -= len(chunk)
        except aiohttp.EofStream:
            raise errors.IncompleteRead(length-required, required)

    def parse_eof_payload(self, out, buf):
        """Read all bytes untile eof."""
        try:
            while True:
                out.feed_data((yield from buf.readsome()))
        except aiohttp.EofStream:
            pass
