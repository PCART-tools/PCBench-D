    def _open(self) -> None:
        # Header
        assert self.fp is not None

        s = self.fp.read(32)
        if not _accept(s):
            msg = "not an MSP file"
            raise SyntaxError(msg)

        # Header checksum
        checksum = 0
        for i in range(0, 32, 2):
            checksum = checksum ^ i16(s, i)
        if checksum != 0:
            msg = "bad MSP checksum"
            raise SyntaxError(msg)

        self._mode = "1"
        self._size = i16(s, 4), i16(s, 6)

        if s.startswith(b"DanM"):
            self.tile = [ImageFile._Tile("raw", (0, 0) + self.size, 32, "1")]
        else:
            self.tile = [ImageFile._Tile("MSP", (0, 0) + self.size, 32)]
