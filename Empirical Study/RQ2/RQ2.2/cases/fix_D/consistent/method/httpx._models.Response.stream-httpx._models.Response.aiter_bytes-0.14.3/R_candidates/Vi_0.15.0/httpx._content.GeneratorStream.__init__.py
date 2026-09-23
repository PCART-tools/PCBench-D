    def __init__(self, generator: Iterable[bytes]) -> None:
        self._generator = generator
        self._is_stream_consumed = False
