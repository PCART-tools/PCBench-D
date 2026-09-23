    def parse_headers(self, lines):
        """Parses RFC 5322 headers from a stream.

        Line continuations are supported. Returns list of header name
        and value pairs. Header name is in upper case.
        """
        headers = CIMultiDict()
        raw_headers = []

        lines_idx = 1
        line = lines[1]
        line_count = len(lines)

        while line:
            header_length = len(line)

            # Parse initial header name : value pair.
            try:
                bname, bvalue = line.split(b':', 1)
            except ValueError:
                raise InvalidHeader(line) from None

            bname = bname.strip(b' \t')
            if HDRRE.search(bname):
                raise InvalidHeader(bname)

            # next line
            lines_idx += 1
            line = lines[lines_idx]

            # consume continuation lines
            continuation = line and line[0] in (32, 9)  # (' ', '\t')

            if continuation:
                bvalue = [bvalue]
                while continuation:
                    header_length += len(line)
                    if header_length > self.max_field_size:
                        raise LineTooLong(
                            'request header field {}'.format(
                                bname.decode("utf8", "xmlcharrefreplace")),
                            self.max_field_size)
                    bvalue.append(line)

                    # next line
                    lines_idx += 1
                    if lines_idx < line_count:
                        line = lines[lines_idx]
                        if line:
                            continuation = line[0] in (32, 9)  # (' ', '\t')
                    else:
                        line = b''
                        break
                bvalue = b''.join(bvalue)
            else:
                if header_length > self.max_field_size:
                    raise LineTooLong(
                        'request header field {}'.format(
                            bname.decode("utf8", "xmlcharrefreplace")),
                        self.max_field_size)

            bvalue = bvalue.strip()
            name = bname.decode('utf-8', 'surrogateescape')
            value = bvalue.decode('utf-8', 'surrogateescape')

            headers.add(name, value)
            raw_headers.append((bname, bvalue))

        close_conn = None
        encoding = None
        upgrade = False
        chunked = False
        raw_headers = tuple(raw_headers)

        # keep-alive
        conn = headers.get(hdrs.CONNECTION)
        if conn:
            v = conn.lower()
            if v == 'close':
                close_conn = True
            elif v == 'keep-alive':
                close_conn = False
            elif v == 'upgrade':
                upgrade = True

        # encoding
        enc = headers.get(hdrs.CONTENT_ENCODING)
        if enc:
            enc = enc.lower()
            if enc in ('gzip', 'deflate', 'br'):
                encoding = enc

        # chunking
        te = headers.get(hdrs.TRANSFER_ENCODING)
        if te and 'chunked' in te.lower():
            chunked = True

        return headers, raw_headers, close_conn, encoding, upgrade, chunked
