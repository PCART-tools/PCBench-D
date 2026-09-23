    def __init__(self, agenerator: AsyncIterable[bytes]) -> None:
        self._agenerator = agenerator
        self._is_stream_consumed = False
