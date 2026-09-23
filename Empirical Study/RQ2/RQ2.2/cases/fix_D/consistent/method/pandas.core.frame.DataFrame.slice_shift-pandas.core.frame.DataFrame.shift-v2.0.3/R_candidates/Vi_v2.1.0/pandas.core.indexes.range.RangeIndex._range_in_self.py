    def _range_in_self(self, other: range) -> bool:
        """Check if other range is contained in self"""
        # https://stackoverflow.com/a/32481015
        if not other:
            return True
        if not self._range:
            return False
        if len(other) > 1 and other.step % self._range.step:
            return False
        return other.start in self._range and other[-1] in self._range
