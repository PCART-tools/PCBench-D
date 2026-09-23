    def readline(self):
        """
        Read a line of text.

        :returns: An 8-bit string.
        """
        s = b"" if "b" in self.fh.mode else ""
        newline_character = b"\n" if "b" in self.fh.mode else "\n"
        while True:
            c = self.read(1)
            if not c:
                break
            s = s + c
            if c == newline_character:
                break
        return s
