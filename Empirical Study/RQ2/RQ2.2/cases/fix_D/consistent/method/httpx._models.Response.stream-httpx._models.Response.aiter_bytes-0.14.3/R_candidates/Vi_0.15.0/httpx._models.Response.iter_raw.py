    def iter_raw(self) -> typing.Iterator[bytes]:
        """
        A byte-iterator over the raw response content.
        """
        if self.is_stream_consumed:
            raise StreamConsumed()
        if self.is_closed:
            raise ResponseClosed()
        if not isinstance(self.stream, typing.Iterable):
            raise RuntimeError("Attempted to call a sync iterator on an async stream.")

        self.is_stream_consumed = True
        self._num_bytes_downloaded = 0
        with map_exceptions(HTTPCORE_EXC_MAP, request=self._request):
            for part in self.stream:
                self._num_bytes_downloaded += len(part)
                yield part
        self.close()
