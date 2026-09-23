    def __call__(self, out, buf):
        # read HTTP message (response line + headers)
        try:
            raw_data = yield from buf.readuntil(
                b'\r\n\r\n', self.max_line_size + self.max_headers)
        except errors.LineLimitExceededParserError as exc:
            raise errors.LineTooLong('response header', exc.limit) from None

        lines = raw_data.split(b'\r\n')

        line = lines[0].decode('utf-8', 'surrogateescape')
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
        version = HttpVersion(int(match.group(1)), int(match.group(2)))

        # The status code is a three-digit number
        try:
            status = int(status)
        except ValueError:
            raise errors.BadStatusLine(line) from None

        if status < 100 or status > 999:
            raise errors.BadStatusLine(line)

        # read headers
        headers, raw_headers, close, compression = self.parse_headers(lines)

        if close is None:
            close = version <= HttpVersion10

        out.feed_data(
            RawResponseMessage(
                version, status, reason.strip(),
                headers, raw_headers, close, compression),
            len(raw_data))
        out.feed_eof()
