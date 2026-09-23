    def _open(self) -> None:
        if not _accept(self.fp.read(4)):
            msg = "not a QOI file"
            raise SyntaxError(msg)

        self._size = i32(self.fp.read(4)), i32(self.fp.read(4))

        channels = self.fp.read(1)[0]
        self._mode = "RGB" if channels == 3 else "RGBA"

        self.fp.seek(1, os.SEEK_CUR)  # colorspace
        self.tile = [ImageFile._Tile("qoi", (0, 0) + self._size, self.fp.tell(), None)]
