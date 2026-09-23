    def readlines(self, n: int | None = -1) -> list[AnyStr]:
        """
        Read multiple lines of text.

        :param n: Number of lines to read. If omitted, zero, negative or None,
            read until end of region.
        :returns: A list of 8-bit strings.
        """
        lines = []
        while True:
            s = self.readline()
            if not s:
                break
            lines.append(s)
            if len(lines) == n:
                break
        return lines
