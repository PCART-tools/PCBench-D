    def __getitem__(self, ix: int) -> (
        tuple[
            tuple[int, int],
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            Image.Image,
        ]
        | None
    ):
        return self.glyph[ix]
