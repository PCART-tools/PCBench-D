    def __iter__(self) -> typing.Iterator[bytes]:
        yield self.body
