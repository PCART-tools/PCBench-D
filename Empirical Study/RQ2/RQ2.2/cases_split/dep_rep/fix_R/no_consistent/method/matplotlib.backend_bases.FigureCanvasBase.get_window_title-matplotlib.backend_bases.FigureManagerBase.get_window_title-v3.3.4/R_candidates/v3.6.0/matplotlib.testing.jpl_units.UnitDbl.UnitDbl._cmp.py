    def _cmp(self, op, rhs):
        """Check that *self* and *rhs* share units; compare them using *op*."""
        self.checkSameUnits(rhs, "compare")
        return op(self._value, rhs._value)
