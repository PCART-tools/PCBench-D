    def _open(self) -> None:
        # check magic
        assert self.fp is not None

        if not _accept(self.fp.read(6)):
            msg = "not an XV thumbnail file"
            raise SyntaxError(msg)

        # Skip to beginning of next line
        self.fp.readline()

        # skip info comments
        while True:
            s = self.fp.readline()
            if not s:
                msg = "Unexpected EOF reading XV thumbnail file"
                raise SyntaxError(msg)
            if s[0] != 35:  # ie. when not a comment: '#'
                break

        # parse header line (already read)
        s = s.strip().split()

        self._mode = "P"
        self._size = int(s[0]), int(s[1])

        self.palette = ImagePalette.raw("RGB", PALETTE)

        self.tile = [
            ImageFile._Tile(
                "raw", (0, 0) + self.size, self.fp.tell(), (self.mode, 0, 1)
            )
        ]
