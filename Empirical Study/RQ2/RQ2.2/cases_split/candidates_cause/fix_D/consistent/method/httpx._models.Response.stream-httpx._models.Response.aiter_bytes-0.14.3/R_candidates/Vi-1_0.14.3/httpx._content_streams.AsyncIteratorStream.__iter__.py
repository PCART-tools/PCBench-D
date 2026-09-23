    def __iter__(self) -> typing.Iterator[bytes]:
        raise RuntimeError("Attempted to call a sync iterator on an async stream.")
