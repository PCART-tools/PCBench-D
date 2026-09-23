    @doc(Index.__iter__)
    def __iter__(self) -> Iterator[int]:
        yield from self._range
