    def _binop_unit_unit(self, op, rhs):
        """Check that *self* and *rhs* share units; combine them using *op*."""
        self.checkSameUnits(rhs, op.__name__)
        return UnitDbl(op(self._value, rhs._value), self._units)
