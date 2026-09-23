    def parse_message(self, lines):
        if len(lines[0]) > self.max_line_size:
            raise LineTooLong(
                'Status line is too long', self.max_line_size)

        line = lines[0].decode('utf-8', 'surrogateescape')
        try:
            version, status = line.split(None, 1)
        except ValueError:
            raise BadStatusLine(line) from None
        else:
            try:
                status, reason = status.split(None, 1)
            except ValueError:
                reason = ''

        # version
        match = VERSRE.match(version)
        if match is None:
            raise BadStatusLine(line)
        version = HttpVersion(int(match.group(1)), int(match.group(2)))

        # The status code is a three-digit number
        try:
            status = int(status)
        except ValueError:
            raise BadStatusLine(line) from None

        if status > 999:
            raise BadStatusLine(line)

        # read headers
        headers, raw_headers, \
            close, compression, upgrade, chunked = self.parse_headers(lines)

        if close is None:
            close = version <= HttpVersion10

        return RawResponseMessage(
            version, status, reason.strip(),
            headers, raw_headers, close, compression, upgrade, chunked)
