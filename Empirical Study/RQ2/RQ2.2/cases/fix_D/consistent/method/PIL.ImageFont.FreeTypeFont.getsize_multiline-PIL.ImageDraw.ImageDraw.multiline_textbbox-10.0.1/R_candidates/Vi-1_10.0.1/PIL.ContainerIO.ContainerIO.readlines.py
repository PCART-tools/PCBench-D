    def readlines(self):
        """
        Read multiple lines of text.

        :returns: A list of 8-bit strings.
        """
        lines = []
        while True:
            s = self.readline()
            if not s:
                break
            lines.append(s)
        return lines
