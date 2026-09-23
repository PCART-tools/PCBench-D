class HttpRequestParser(HttpParser):
    """Read request status line. Exception errors.BadStatusLine
    could be raised in case of any errors in status line.
    Returns RawRequestMessage.
    """

    def __call__(self, out, buf):
        try:
            # read http message (request line + headers)
            raw_data = yield from buf.readuntil(
                b'\r\n\r\n', self.max_headers, errors.LineTooLong)
            lines = raw_data.decode(
                'ascii', 'surrogateescape').splitlines(True)

            # request line
            line = lines[0]
            try:
                method, path, version = line.split(None, 2)
            except ValueError:
                raise errors.BadStatusLine(line) from None

            # method
            method = method.upper()
            if not METHRE.match(method):
                raise errors.BadStatusLine(method)

            # version
            match = VERSRE.match(version)
            if match is None:
                raise errors.BadStatusLine(version)
            version = (int(match.group(1)), int(match.group(2)))

            # read headers
            headers, close, compression = self.parse_headers(lines)
            if version <= (1, 0):
                close = True
            elif close is None:
                close = False

            out.feed_data(
                RawRequestMessage(
                    method, path, version, headers, close, compression))
            out.feed_eof()
        except aiohttp.EofStream:
            # Presumably, the server closed the connection before
            # sending a valid response.
            pass
