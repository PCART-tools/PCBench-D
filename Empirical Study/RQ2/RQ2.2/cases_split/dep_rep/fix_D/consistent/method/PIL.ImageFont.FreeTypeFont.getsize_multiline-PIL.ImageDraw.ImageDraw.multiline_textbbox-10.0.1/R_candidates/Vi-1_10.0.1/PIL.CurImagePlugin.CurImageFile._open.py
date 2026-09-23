    def _open(self):
        offset = self.fp.tell()

        # check magic
        s = self.fp.read(6)
        if not _accept(s):
            msg = "not a CUR file"
            raise SyntaxError(msg)

        # pick the largest cursor in the file
        m = b""
        for i in range(i16(s, 4)):
            s = self.fp.read(16)
            if not m:
                m = s
            elif s[0] > m[0] and s[1] > m[1]:
                m = s
        if not m:
            msg = "No cursors were found"
            raise TypeError(msg)

        # load as bitmap
        self._bitmap(i32(m, 12) + offset)

        # patch up the bitmap height
        self._size = self.size[0], self.size[1] // 2
        d, e, o, a = self.tile[0]
        self.tile[0] = d, (0, 0) + self.size, o, a

        return
