    def __call__(self, out, buf):
        # read HTTP message (request line + headers)
        try:
            raw_data = yield from buf.readuntil(
                b'\r\n\r\n', self.max_headers)
        except errors.LineLimitExceededParserError as exc:
            raise errors.LineTooLong('request header', exc.limit) from None

        lines = raw_data.split(b'\r\n')

        # request line
        line = lines[0].decode('utf-8', 'surrogateescape')
        try:
            method, path, version = line.split(None, 2)
        except ValueError:
            raise errors.BadStatusLine(line) from None

        # method
        method = method.upper()
        if not METHRE.match(method):
            raise errors.BadStatusLine(method)

        # version
        try:
            if version.startswith('HTTP/'):
                n1, n2 = version[5:].split('.', 1)
                version = HttpVersion(int(n1), int(n2))
            else:
                raise errors.BadStatusLine(version)
        except:
            raise errors.BadStatusLine(version)

        # read headers
        headers, raw_headers, close, compression = self.parse_headers(lines)
        if close is None:  # then the headers weren't set in the request
            if version <= HttpVersion10:  # HTTP 1.0 must asks to not close
                close = True
            else:  # HTTP 1.1 must ask to close.
                close = False

        out.feed_data(
            RawRequestMessage(
                method, path, version, headers, raw_headers,
                close, compression),
            len(raw_data))
        out.feed_eof()
