    def feed_eof(self):
        if self._payload_parser is not None:
            self._payload_parser.feed_eof()
            self._payload_parser = None
        else:
            # try to extract partial message
            if self._tail:
                self._lines.append(self._tail)

            if self._lines:
                if self._lines[-1] != '\r\n':
                    self._lines.append('')
                try:
                    return self.parse_message(self._lines)
                except:
                    return None
