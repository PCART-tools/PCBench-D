    def _open(self) -> None:
        if not _accept(self.fp.read(4)):
            msg = "not an FTEX file"
            raise SyntaxError(msg)
        struct.unpack("<i", self.fp.read(4))  # version
        self._size = struct.unpack("<2i", self.fp.read(8))
        mipmap_count, format_count = struct.unpack("<2i", self.fp.read(8))

        self._mode = "RGB"

        # Only support single-format files.
        # I don't know of any multi-format file.
        assert format_count == 1

        format, where = struct.unpack("<2i", self.fp.read(8))
        self.fp.seek(where)
        (mipmap_size,) = struct.unpack("<i", self.fp.read(4))

        data = self.fp.read(mipmap_size)

        if format == Format.DXT1:
            self._mode = "RGBA"
            self.tile = [("bcn", (0, 0) + self.size, 0, 1)]
        elif format == Format.UNCOMPRESSED:
            self.tile = [("raw", (0, 0) + self.size, 0, ("RGB", 0, 1))]
        else:
            msg = f"Invalid texture compression format: {repr(format)}"
            raise ValueError(msg)

        self.fp.close()
        self.fp = BytesIO(data)
