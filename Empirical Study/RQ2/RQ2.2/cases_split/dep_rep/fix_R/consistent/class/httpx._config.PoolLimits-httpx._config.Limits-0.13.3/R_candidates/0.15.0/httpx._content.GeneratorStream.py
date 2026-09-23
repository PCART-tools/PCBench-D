class GeneratorStream:
    """
    Request content encoded as plain bytes, using an byte generator.
    """

    def __init__(self, generator: Iterable[bytes]) -> None:
        self._generator = generator
        self._is_stream_consumed = False

    def __iter__(self) -> Iterator[bytes]:
        if self._is_stream_consumed:
            raise StreamConsumed()

        self._is_stream_consumed = True
        for part in self._generator:
            yield part
