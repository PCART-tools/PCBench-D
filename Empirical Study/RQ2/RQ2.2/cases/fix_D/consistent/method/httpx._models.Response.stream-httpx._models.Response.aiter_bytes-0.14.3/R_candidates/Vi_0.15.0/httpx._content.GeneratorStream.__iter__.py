    def __iter__(self) -> Iterator[bytes]:
        if self._is_stream_consumed:
            raise StreamConsumed()

        self._is_stream_consumed = True
        for part in self._generator:
            yield part
