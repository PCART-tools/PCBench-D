    def read(self, n: int = 0) -> AnyStr:
        """
        Read data.

        :param n: Number of bytes to read. If omitted or zero,
            read until end of region.
        :returns: An 8-bit string.
        """
        if n:
            n = min(n, self.length - self.pos)
        else:
            n = self.length - self.pos
        if not n:  # EOF
            return b"" if "b" in self.fh.mode else ""  # type: ignore[return-value]
        self.pos = self.pos + n
        return self.fh.read(n)
