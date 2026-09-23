    def feed_eof(self):
        if self._payload_parser is not None:
            self._payload_parser.feed_eof()
            self._payload_parser = None
