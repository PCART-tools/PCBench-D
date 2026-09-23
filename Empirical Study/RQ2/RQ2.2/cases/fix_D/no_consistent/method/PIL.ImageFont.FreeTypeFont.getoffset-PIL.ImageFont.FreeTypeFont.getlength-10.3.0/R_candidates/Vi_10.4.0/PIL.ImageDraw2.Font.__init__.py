    def __init__(
        self, color: str, file: StrOrBytesPath | BinaryIO, size: float = 12
    ) -> None:
        # FIXME: add support for bitmap fonts
        self.color = ImageColor.getrgb(color)
        self.font = ImageFont.truetype(file, size)
