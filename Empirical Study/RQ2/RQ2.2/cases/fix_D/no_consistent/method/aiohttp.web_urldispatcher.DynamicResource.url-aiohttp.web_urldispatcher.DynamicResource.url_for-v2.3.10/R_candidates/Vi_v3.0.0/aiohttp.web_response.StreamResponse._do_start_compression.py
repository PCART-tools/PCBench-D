    def _do_start_compression(self, coding):
        if coding != ContentCoding.identity:
            self.headers[hdrs.CONTENT_ENCODING] = coding.value
            self._payload_writer.enable_compression(coding.value)
            # Compressed payload may have different content length,
            # remove the header
            self._headers.popall(hdrs.CONTENT_LENGTH, None)
