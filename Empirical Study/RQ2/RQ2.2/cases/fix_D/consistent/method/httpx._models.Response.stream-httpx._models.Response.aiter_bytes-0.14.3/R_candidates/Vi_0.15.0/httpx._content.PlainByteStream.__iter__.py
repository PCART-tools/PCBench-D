    def __iter__(self) -> Iterator[bytes]:
        yield self._body
