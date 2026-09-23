    @palette.setter
    def palette(self, palette: Sequence[int] | bytes | bytearray) -> None:
        self._colors: dict[tuple[int, ...], int] | None = None
        self._palette = palette
