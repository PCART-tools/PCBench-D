    def add_header(self, name, value):
        """Analyze headers. Calculate content length,
        removes hop headers, etc."""
        assert not self.headers_sent, 'headers have been sent already'
        assert isinstance(name, str), \
            'Header name should be a string, got {!r}'.format(name)
        assert set(name).issubset(ASCIISET), \
            'Header name should contain ASCII chars, got {!r}'.format(name)
        assert isinstance(value, str), \
            'Header {!r} should have string value, got {!r}'.format(
                name, value)

        name = istr(name)
        value = value.strip()

        if name == hdrs.CONTENT_LENGTH:
            self.length = int(value)

        if name == hdrs.TRANSFER_ENCODING:
            self.has_chunked_hdr = value.lower().strip() == 'chunked'

        if name == hdrs.CONNECTION:
            val = value.lower()
            # handle websocket
            if 'upgrade' in val:
                self.upgrade = True
            # connection keep-alive
            elif 'close' in val:
                self.keepalive = False
            elif 'keep-alive' in val:
                self.keepalive = True

        elif name == hdrs.UPGRADE:
            if 'websocket' in value.lower():
                self.websocket = True
                self.headers[name] = value

        elif name not in self.HOP_HEADERS:
            # ignore hop-by-hop headers
            self.headers.add(name, value)
