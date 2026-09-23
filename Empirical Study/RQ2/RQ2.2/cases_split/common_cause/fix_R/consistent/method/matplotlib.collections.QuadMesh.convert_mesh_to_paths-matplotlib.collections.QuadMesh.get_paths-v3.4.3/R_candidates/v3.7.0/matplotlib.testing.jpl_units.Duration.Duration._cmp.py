    def _cmp(self, op, rhs):
        """
        Check that *self* and *rhs* share frames; compare them using *op*.
        """
        self.checkSameFrame(rhs, "compare")
        return op(self._seconds, rhs._seconds)
