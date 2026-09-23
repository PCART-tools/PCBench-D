    def __iter__(self) -> typing.Iterator[bytes]:
        if self.is_stream_consumed:
            raise StreamConsumed()
        self.is_stream_consumed = True
        for part in self.iterator:
            yield part
