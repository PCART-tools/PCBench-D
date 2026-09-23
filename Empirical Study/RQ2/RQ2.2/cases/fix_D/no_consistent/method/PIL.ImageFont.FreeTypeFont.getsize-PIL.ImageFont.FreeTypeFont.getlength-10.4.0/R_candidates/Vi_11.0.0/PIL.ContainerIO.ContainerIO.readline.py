    def readline(self, n: int = -1) -> AnyStr:
        """
        Read a line of text.

        :param n: Number of bytes to read. If omitted, zero or negative,
            read until end of line.
        :returns: An 8-bit string.
        """
        s: AnyStr = b"" if "b" in self.fh.mode else ""  # type: ignore[assignment]
        newline_character = b"\n" if "b" in self.fh.mode else "\n"
        while True:
            c = self.read(1)
            if not c:
                break
            s = s + c
            if c == newline_character or len(s) == n:
                break
        return s
