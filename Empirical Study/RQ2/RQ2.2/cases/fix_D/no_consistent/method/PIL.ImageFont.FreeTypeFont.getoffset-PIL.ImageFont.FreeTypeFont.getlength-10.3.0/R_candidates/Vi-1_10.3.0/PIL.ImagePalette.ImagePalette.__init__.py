    def __init__(self, mode: str = "RGB", palette: Sequence[int] | None = None) -> None:
        self.mode = mode
        self.rawmode = None  # if set, palette contains raw data
        self.palette = palette or bytearray()
        self.dirty: int | None = None
