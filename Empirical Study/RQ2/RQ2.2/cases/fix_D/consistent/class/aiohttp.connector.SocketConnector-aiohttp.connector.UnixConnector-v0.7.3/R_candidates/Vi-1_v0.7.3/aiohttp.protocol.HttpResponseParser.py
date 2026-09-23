class HttpResponseParser(HttpParser):
    """Read response status line and headers.

    BadStatusLine  could be raised in case of any errors in status line.
    Returns RawResponseMessage"""

    def __call__(self, out, buf):
        try:
            # read http message (response line + headers)
            raw_data = yield from buf.readuntil(
                b'\r\n\r\n', self.max_line_size+self.max_headers,
                errors.LineTooLong)
            lines = raw_data.decode(
                'ascii', 'surrogateescape').splitlines(True)

            line = lines[0]
            try:
                version, status = line.split(None, 1)
            except ValueError:
                raise errors.BadStatusLine(line) from None
            else:
                try:
                    status, reason = status.split(None, 1)
                except ValueError:
                    reason = ''

            # version
            match = VERSRE.match(version)
            if match is None:
                raise errors.BadStatusLine(line)
            version = (int(match.group(1)), int(match.group(2)))

            # The status code is a three-digit number
            try:
                status = int(status)
            except ValueError:
                raise errors.BadStatusLine(line) from None

            if status < 100 or status > 999:
                raise errors.BadStatusLine(line)

            # read headers
            headers, close, compression = self.parse_headers(lines)

            if close is None:
                close = version <= (1, 0)

            out.feed_data(
                RawResponseMessage(
                    version, status, reason.strip(),
                    headers, close, compression))
            out.feed_eof()
        except aiohttp.EofStream:
            # Presumably, the server closed the connection before
            # sending a valid response.
            raise errors.BadStatusLine(b'') from None
