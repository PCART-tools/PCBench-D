    def __init__(self, value, *args, **kwargs):
        assert isinstance(value, (bytes, bytearray, memoryview)), \
            "value argument must be byte-ish (%r)" % type(value)

        if 'content_type' not in kwargs:
            kwargs['content_type'] = 'application/octet-stream'

        super().__init__(value, *args, **kwargs)

        self._size = len(value)

        if self._size > TOO_LARGE_BYTES_BODY:
            warnings.warn("Sending a large body directly with raw bytes might"
                          " lock the event loop. You should probably pass an "
                          "io.BytesIO object instead", ResourceWarning)
