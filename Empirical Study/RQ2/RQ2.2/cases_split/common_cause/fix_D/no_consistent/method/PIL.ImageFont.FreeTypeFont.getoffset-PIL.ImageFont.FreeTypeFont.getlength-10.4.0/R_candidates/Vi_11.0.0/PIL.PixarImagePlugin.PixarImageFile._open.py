    def _open(self) -> None:
        # assuming a 4-byte magic label
        assert self.fp is not None

        s = self.fp.read(4)
        if not _accept(s):
            msg = "not a PIXAR file"
            raise SyntaxError(msg)

        # read rest of header
        s = s + self.fp.read(508)

        self._size = i16(s, 418), i16(s, 416)

        # get channel/depth descriptions
        mode = i16(s, 424), i16(s, 426)

        if mode == (14, 2):
            self._mode = "RGB"
        # FIXME: to be continued...

        # create tile descriptor (assuming "dumped")
        self.tile = [
            ImageFile._Tile("raw", (0, 0) + self.size, 1024, (self.mode, 0, 1))
        ]
