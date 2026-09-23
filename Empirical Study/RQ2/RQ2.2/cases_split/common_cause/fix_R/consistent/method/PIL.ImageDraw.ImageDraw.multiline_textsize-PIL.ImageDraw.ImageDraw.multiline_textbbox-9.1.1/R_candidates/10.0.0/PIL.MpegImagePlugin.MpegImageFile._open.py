    def _open(self):
        s = BitStream(self.fp)

        if s.read(32) != 0x1B3:
            msg = "not an MPEG file"
            raise SyntaxError(msg)

        self.mode = "RGB"
        self._size = s.read(12), s.read(12)
