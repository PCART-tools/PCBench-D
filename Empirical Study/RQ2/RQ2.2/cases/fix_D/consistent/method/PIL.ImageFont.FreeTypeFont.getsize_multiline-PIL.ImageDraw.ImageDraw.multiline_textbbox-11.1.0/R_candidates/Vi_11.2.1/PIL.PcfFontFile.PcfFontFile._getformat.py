    def _getformat(
        self, tag: int
    ) -> tuple[BinaryIO, int, Callable[[bytes], int], Callable[[bytes], int]]:
        format, size, offset = self.toc[tag]

        fp = self.fp
        fp.seek(offset)

        format = l32(fp.read(4))

        if format & 4:
            i16, i32 = b16, b32
        else:
            i16, i32 = l16, l32

        return fp, format, i16, i32
