    def __init__(
        self, aiterator: typing.AsyncIterator[bytes], close_func: typing.Callable = None
    ) -> None:
        self.aiterator = aiterator
        self.close_func = close_func
        self.is_stream_consumed = False
