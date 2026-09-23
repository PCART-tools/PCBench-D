    def equals(self, other):
        """
        Determines if two Index objects contain the same elements.
        """
        if isinstance(other, RangeIndex):
            ls = len(self)
            lo = len(other)
            return (ls == lo == 0 or
                    ls == lo == 1 and
                    self._start == other._start or
                    ls == lo and
                    self._start == other._start and
                    self._step == other._step)

        return super(RangeIndex, self).equals(other)
