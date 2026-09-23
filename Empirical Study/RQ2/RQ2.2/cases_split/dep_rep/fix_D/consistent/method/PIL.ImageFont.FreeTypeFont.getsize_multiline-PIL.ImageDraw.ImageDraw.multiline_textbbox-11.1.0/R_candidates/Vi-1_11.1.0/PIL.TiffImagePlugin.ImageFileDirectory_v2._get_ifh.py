    def _get_ifh(self):
        ifh = self._prefix + self._pack("H", 43 if self._bigtiff else 42)
        if self._bigtiff:
            ifh += self._pack("HH", 8, 0)
        ifh += self._pack("Q", 16) if self._bigtiff else self._pack("L", 8)

        return ifh
