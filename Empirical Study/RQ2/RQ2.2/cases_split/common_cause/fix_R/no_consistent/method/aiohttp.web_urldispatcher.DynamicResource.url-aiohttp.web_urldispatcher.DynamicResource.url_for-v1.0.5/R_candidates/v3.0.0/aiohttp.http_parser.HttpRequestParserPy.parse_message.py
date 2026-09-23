    def parse_message(self, lines):
        if len(lines[0]) > self.max_line_size:
            raise LineTooLong(
                'Status line is too long', self.max_line_size)

        # request line
        line = lines[0].decode('utf-8', 'surrogateescape')
        try:
            method, path, version = line.split(None, 2)
        except ValueError:
            raise BadStatusLine(line) from None

        # method
        method = method.upper()
        if not METHRE.match(method):
            raise BadStatusLine(method)

        # version
        try:
            if version.startswith('HTTP/'):
                n1, n2 = version[5:].split('.', 1)
                version = HttpVersion(int(n1), int(n2))
            else:
                raise BadStatusLine(version)
        except Exception:
            raise BadStatusLine(version)

        # read headers
        headers, raw_headers, \
            close, compression, upgrade, chunked = self.parse_headers(lines)

        if close is None:  # then the headers weren't set in the request
            if version <= HttpVersion10:  # HTTP 1.0 must asks to not close
                close = True
            else:  # HTTP 1.1 must ask to close.
                close = False

        return RawRequestMessage(
            method, path, version, headers, raw_headers,
            close, compression, upgrade, chunked, URL(path))
