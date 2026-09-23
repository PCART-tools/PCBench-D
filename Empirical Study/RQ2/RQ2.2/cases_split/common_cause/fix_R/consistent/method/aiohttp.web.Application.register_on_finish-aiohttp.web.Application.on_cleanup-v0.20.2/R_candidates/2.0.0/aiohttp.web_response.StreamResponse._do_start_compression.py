    def _do_start_compression(self, coding):
        if coding != ContentCoding.identity:
            self.headers[hdrs.CONTENT_ENCODING] = coding.value
            self._payload_writer.enable_compression(coding.value)
            self._chunked = True
