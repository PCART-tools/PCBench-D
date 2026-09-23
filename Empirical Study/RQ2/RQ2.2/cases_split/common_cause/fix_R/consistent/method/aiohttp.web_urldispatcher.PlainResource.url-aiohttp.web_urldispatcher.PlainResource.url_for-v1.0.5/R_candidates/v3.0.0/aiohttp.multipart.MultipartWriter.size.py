    @property
    def size(self):
        """Size of the payload."""
        if not self._parts:
            return 0

        total = 0
        for part, headers, encoding, te_encoding in self._parts:
            if encoding or te_encoding or part.size is None:
                return None

            total += (
                2 + len(self._boundary) + 2 +  # b'--'+self._boundary+b'\r\n'
                part.size + len(headers) +
                2  # b'\r\n'
            )

        total += 2 + len(self._boundary) + 4  # b'--'+self._boundary+b'--\r\n'
        return total
