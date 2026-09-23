    def readline(self) -> AnyStr:
        """
        Read a line of text.

        :returns: An 8-bit string.
        """
        s: AnyStr = b"" if "b" in self.fh.mode else ""  # type: ignore[assignment]
        newline_character = b"\n" if "b" in self.fh.mode else "\n"
        while True:
            c = self.read(1)
            if not c:
                break
            s = s + c
            if c == newline_character:
                break
        return s
