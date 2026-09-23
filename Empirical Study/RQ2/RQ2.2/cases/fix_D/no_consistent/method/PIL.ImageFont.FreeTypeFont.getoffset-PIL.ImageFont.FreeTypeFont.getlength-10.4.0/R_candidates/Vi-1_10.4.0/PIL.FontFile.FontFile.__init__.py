    def __init__(self) -> None:
        self.info: dict[bytes, bytes | int] = {}
        self.glyph: list[
            tuple[
                tuple[int, int],
                tuple[int, int, int, int],
                tuple[int, int, int, int],
                Image.Image,
            ]
            | None
        ] = [None] * 256
