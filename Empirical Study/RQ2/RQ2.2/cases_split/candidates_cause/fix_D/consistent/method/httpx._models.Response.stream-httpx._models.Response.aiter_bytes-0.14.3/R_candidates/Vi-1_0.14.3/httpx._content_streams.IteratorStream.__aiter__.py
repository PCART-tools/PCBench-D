    def __aiter__(self) -> typing.AsyncIterator[bytes]:
        raise RuntimeError("Attempted to call a async iterator on an sync stream.")
