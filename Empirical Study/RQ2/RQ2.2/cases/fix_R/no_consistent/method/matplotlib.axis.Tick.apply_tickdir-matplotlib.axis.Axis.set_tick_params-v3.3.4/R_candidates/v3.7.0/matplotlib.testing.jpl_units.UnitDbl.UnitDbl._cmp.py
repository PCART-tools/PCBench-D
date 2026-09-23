    def _cmp(self, op, rhs):
        """Check that *self* and *rhs* share units; compare them using *op*."""
        if rhs is None:
            return NotImplemented
        self.checkSameUnits(rhs, "compare")
        return op(self._value, rhs._value)
