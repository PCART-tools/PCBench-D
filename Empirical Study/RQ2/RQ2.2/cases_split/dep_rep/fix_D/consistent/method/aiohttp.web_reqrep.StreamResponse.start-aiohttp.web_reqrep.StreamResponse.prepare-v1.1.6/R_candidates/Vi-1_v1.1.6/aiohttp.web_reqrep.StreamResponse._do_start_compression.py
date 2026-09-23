    def _do_start_compression(self, coding):
        if coding != ContentCoding.identity:
            self.headers[hdrs.CONTENT_ENCODING] = coding.value
            self._resp_impl.add_compression_filter(coding.value)
            self.content_length = None
