    def write(self, data):
        assert isinstance(data, (bytes, bytearray, memoryview)), \
            "data argument must be byte-ish (%r)" % type(data)

        if self._eof_sent:
            raise RuntimeError("Cannot call write() after write_eof()")
        if self._resp_impl is None:
            raise RuntimeError("Cannot call write() before start()")

        if data:
            return self._resp_impl.write(data)
        else:
            return ()
