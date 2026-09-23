    def __init__(
        self, iterator: typing.Iterator[bytes], close_func: typing.Callable = None
    ) -> None:
        self.iterator = iterator
        self.close_func = close_func
        self.is_stream_consumed = False
