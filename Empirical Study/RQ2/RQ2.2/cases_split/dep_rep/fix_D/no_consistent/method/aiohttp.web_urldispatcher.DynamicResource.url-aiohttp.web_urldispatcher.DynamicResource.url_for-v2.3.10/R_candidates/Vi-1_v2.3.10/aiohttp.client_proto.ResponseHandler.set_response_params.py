    def set_response_params(self, *, timer=None,
                            skip_payload=False,
                            skip_status_codes=(),
                            read_until_eof=False,
                            auto_decompress=True):
        self._skip_payload = skip_payload
        self._skip_status_codes = skip_status_codes
        self._read_until_eof = read_until_eof
        self._parser = HttpResponseParser(
            self, self._loop, timer=timer,
            payload_exception=ClientPayloadError,
            read_until_eof=read_until_eof,
            auto_decompress=auto_decompress)

        if self._tail:
            data, self._tail = self._tail, b''
            self.data_received(data)
