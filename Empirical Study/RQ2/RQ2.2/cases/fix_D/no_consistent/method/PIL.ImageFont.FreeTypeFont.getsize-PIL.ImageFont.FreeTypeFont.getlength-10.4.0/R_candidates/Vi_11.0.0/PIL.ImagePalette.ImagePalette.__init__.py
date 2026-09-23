    def __init__(
        self,
        mode: str = "RGB",
        palette: Sequence[int] | bytes | bytearray | None = None,
    ) -> None:
        self.mode = mode
        self.rawmode: str | None = None  # if set, palette contains raw data
        self.palette = palette or bytearray()
        self.dirty: int | None = None
