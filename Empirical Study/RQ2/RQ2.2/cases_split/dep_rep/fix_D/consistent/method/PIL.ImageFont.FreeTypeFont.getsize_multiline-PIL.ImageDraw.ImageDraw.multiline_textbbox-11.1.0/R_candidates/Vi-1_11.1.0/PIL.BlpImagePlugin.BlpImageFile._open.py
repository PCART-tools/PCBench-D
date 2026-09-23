    def _open(self) -> None:
        self.magic = self.fp.read(4)
        if not _accept(self.magic):
            msg = f"Bad BLP magic {repr(self.magic)}"
            raise BLPFormatError(msg)

        compression = struct.unpack("<i", self.fp.read(4))[0]
        if self.magic == b"BLP1":
            alpha = struct.unpack("<I", self.fp.read(4))[0] != 0
        else:
            encoding = struct.unpack("<b", self.fp.read(1))[0]
            alpha = struct.unpack("<b", self.fp.read(1))[0] != 0
            alpha_encoding = struct.unpack("<b", self.fp.read(1))[0]
            self.fp.seek(1, os.SEEK_CUR)  # mips

        self._size = struct.unpack("<II", self.fp.read(8))

        args: tuple[int, int, bool] | tuple[int, int, bool, int]
        if self.magic == b"BLP1":
            encoding = struct.unpack("<i", self.fp.read(4))[0]
            self.fp.seek(4, os.SEEK_CUR)  # subtype

            args = (compression, encoding, alpha)
            offset = 28
        else:
            args = (compression, encoding, alpha, alpha_encoding)
            offset = 20

        decoder = self.magic.decode()

        self._mode = "RGBA" if alpha else "RGB"
        self.tile = [ImageFile._Tile(decoder, (0, 0) + self.size, offset, args)]
