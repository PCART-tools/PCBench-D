    def parse_headers(self, lines):
        """Parses RFC 5322 headers from a stream.

        Line continuations are supported. Returns list of header name
        and value pairs. Header name is in upper case.
        """
        close_conn = None
        encoding = None
        headers = CIMultiDict()
        raw_headers = []

        lines_idx = 1
        line = lines[1]

        while line:
            header_length = len(line)

            # Parse initial header name : value pair.
            try:
                bname, bvalue = line.split(b':', 1)
            except ValueError:
                raise errors.InvalidHeader(line) from None

            bname = bname.strip(b' \t').upper()
            if HDRRE.search(bname):
                raise errors.InvalidHeader(bname)

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
                        raise errors.LineTooLong(
                            'request header field {}'.format(
                                bname.decode("utf8", "xmlcharrefreplace")),
                            self.max_field_size)
                    bvalue.append(line)

                    # next line
                    lines_idx += 1
                    line = lines[lines_idx]
                    continuation = line[0] in (32, 9)  # (' ', '\t')
                bvalue = b'\r\n'.join(bvalue)
            else:
                if header_length > self.max_field_size:
                    raise errors.LineTooLong(
                        'request header field {}'.format(
                            bname.decode("utf8", "xmlcharrefreplace")),
                        self.max_field_size)

            bvalue = bvalue.strip()

            name = istr(bname.decode('utf-8', 'surrogateescape'))
            value = bvalue.decode('utf-8', 'surrogateescape')

            # keep-alive and encoding
            if name == hdrs.CONNECTION:
                v = value.lower()
                if v == 'close':
                    close_conn = True
                elif v == 'keep-alive':
                    close_conn = False
            elif name == hdrs.CONTENT_ENCODING:
                enc = value.lower()
                if enc in ('gzip', 'deflate'):
                    encoding = enc

            headers.add(name, value)
            raw_headers.append((bname, bvalue))

        return headers, raw_headers, close_conn, encoding
