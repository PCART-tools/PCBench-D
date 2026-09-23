    def _open(self):
        if not _accept(self.fp.read(4)):
            msg = "not a QOI file"
            raise SyntaxError(msg)

        self._size = tuple(i32(self.fp.read(4)) for i in range(2))

        channels = self.fp.read(1)[0]
        self.mode = "RGB" if channels == 3 else "RGBA"

        self.fp.seek(1, os.SEEK_CUR)  # colorspace
        self.tile = [("qoi", (0, 0) + self._size, self.fp.tell(), None)]
